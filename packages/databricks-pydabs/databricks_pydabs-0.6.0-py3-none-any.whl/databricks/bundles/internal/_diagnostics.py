import json
import os
import traceback
from contextlib import contextmanager
from dataclasses import dataclass, field, replace
from enum import Enum
from io import StringIO
from typing import IO, TYPE_CHECKING, Callable, Iterator, Optional, TypeVar

T = TypeVar("T")

if TYPE_CHECKING:
    from typing_extensions import Self


class Severity(Enum):
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class Location:
    file: str
    line: int
    column: int

    @staticmethod
    def from_callable(fn: Callable) -> Optional["Location"]:
        """
        Capture location of callable. This is useful for creating
        diagnostics of decorated functions.
        """

        code = hasattr(fn, "__code__") and getattr(fn, "__code__")

        if not code:
            return None

        file = code.co_filename
        if file and file.startswith(os.getcwd()):
            # simplify path if we can
            file = os.path.relpath(file, os.getcwd())

        return Location(
            file=file,
            line=code.co_firstlineno,
            column=1,  # there is no way to get column
        )

    def to_text(self) -> str:
        return ":".join(
            [
                self.file,
                str(self.line),
                str(self.column),
            ]
        )

    def to_json(self) -> dict:
        return {
            "file": self.file,
            "line": self.line,
            "column": self.column,
        }


@dataclass(kw_only=True, frozen=True)
class Diagnostic:
    severity: Severity
    summary: str
    detail: Optional[str] = None
    path: Optional[str] = None
    location: Optional[Location] = None

    def to_json(self) -> dict:
        def omit_none(values: dict):
            return {key: value for key, value in values.items() if value is not None}

        if self.location:
            location = self.location.to_json()
        else:
            location = None

        return omit_none(
            {
                "severity": self.severity.value,
                "summary": self.summary,
                "detail": self.detail,
                "path": self.path,
                "location": location,
            }
        )


@dataclass
class Diagnostics:
    """
    Diagnostics is a collection of errors and warnings we print to users.
    """

    items: list[Diagnostic] = field(default_factory=list, kw_only=False)

    def extend(self, diagnostics: "Diagnostics"):
        """
        Extend items with another diagnostics. This pattern allows
        to accumulate errors and warnings.

        Example:

            ```
            def foo() -> Diagnostics: ...
            def bar() -> Diagnostics: ...

            diagnostics = Diagnostics()
            diagnostics = diagnostics.extend(foo())
            diagnostics = diagnostics.extend(bar())
            ```

        """

        return Diagnostics(
            items=[*self.items, *diagnostics.items],
        )

    def extend_tuple(self, pair: tuple[T, "Diagnostics"]) -> tuple[T, "Diagnostics"]:
        """
        Extend items with another diagnostics. This variant is useful when
        methods return a pair of value and diagnostics. This pattern allows
        to accumulate errors and warnings.

        Example:

            ```
            def foo() -> (int, Diagnostics): ...

            diagnostics = Diagnostics()
            value, diagnostics = diagnostics.extend_tuple(foo())
            ```
        """

        value, other_diagnostics = pair

        return value, self.extend(other_diagnostics)

    def with_location_if_absent(self, location: Optional[Location]) -> "Self":
        """
        Add location to diagnostics if it's missing.
        """

        return replace(
            self,
            items=[
                replace(item, location=location) if item.location is None else item
                for item in self.items
            ],
        )

    def has_error(self):
        for item in self.items:
            if item.severity == Severity.ERROR:
                return True

        return False

    @staticmethod
    def create_error(
        msg: str, *, location: Optional[Location] = None, detail: Optional[str] = None
    ):
        return Diagnostics(
            items=[
                Diagnostic(
                    severity=Severity.ERROR,
                    summary=msg,
                    detail=detail,
                    location=location,
                )
            ]
        )

    @staticmethod
    def create_warning(
        msg: str,
        *,
        detail: Optional[str] = None,
        location: Optional[Location] = None,
    ):
        return Diagnostics(
            items=[
                Diagnostic(
                    severity=Severity.WARNING,
                    summary=msg,
                    detail=detail,
                    location=location,
                )
            ]
        )

    @staticmethod
    def from_exception(
        exc: Exception,
        *,
        summary: str,
        location: Optional[Location] = None,
        path: Optional[str] = None,
    ) -> "Diagnostics":
        detail = StringIO()
        traceback.print_exception(exc, file=detail)

        diagnostic = Diagnostic(
            severity=Severity.ERROR,
            summary=summary,
            location=location,
            path=path,
            detail=detail.getvalue(),
        )

        return Diagnostics(items=[diagnostic])

    @contextmanager
    def catch_exceptions(
        *,
        summary: str,
        diagnostics: "Diagnostics",
        location: Optional[Location] = None,
        path: Optional[str] = None,
    ) -> Iterator["Diagnostics"]:
        """
        Catch exceptions and add them to diagnostics.

        Example:

            ```
            diagnostics = Diagnostics()

            with diagnostics.catch_exceptions(
                summary="load bundle",
                # append error to the existing diagnostics
                diagnostics=diagnostics,
            ) as diagnostics:
                ...
            ```
        """

        new_diagnostics = replace(diagnostics)  # copy

        try:
            yield new_diagnostics
        except Exception as exc:
            diagnostics = diagnostics.extend(
                Diagnostics.from_exception(
                    exc=exc, summary=summary, location=location, path=path
                )
            )

            # mutate in-place because we already yielded
            # and contextmanager doesn't allow to yield twice
            new_diagnostics.items = diagnostics.items

    def write_json(self, file: IO):
        """
        Write diagnostics to a format CLI can understand.
        """

        for diagnostic in self.items:
            json.dump(diagnostic.to_json(), file)
            file.write("\n")
