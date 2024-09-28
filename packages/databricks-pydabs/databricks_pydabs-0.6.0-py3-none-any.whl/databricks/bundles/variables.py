import typing
from contextlib import contextmanager
from dataclasses import dataclass, fields, is_dataclass
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "Variable",
    "VariableOr",
    "VariableOrOptional",
    "Bundle",
    "resolve_variable",
    "variables",
]

T = TypeVar("T", covariant=True)

VAR_PREFIX = "var"


@dataclass(kw_only=True)
class Variable(Generic[T]):
    """
    Reference to a bundle variable.

    Instances should be created using :func:`@variables <databricks.bundles.variables.variables>` decorator.

    See: `Databricks Asset Bundles configuration <https://docs.databricks.com/en/dev-tools/bundles/settings.html>`_
    """

    path: str
    """
    Path to the variable, e.g. "var.my_variable".
    """

    type: Type[T] | Any
    """
    Type of the variable or :class:`~Any` if type is unknown.
    """

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def get(self) -> T:
        """
        Returns the value of the variable. This method can only be called
        within :func:`@job <databricks.bundles.jobs.job>`,
        :func:`@resource_generator <databricks.bundles.resource.resource_generator>` or
        :func:`@job_mutator <databricks.bundles.jobs.job_mutator>`.

        You can only get variables starting with "var.".
        """

        return VariableContext.get(self)

    @property
    def value(self) -> str:
        """
        Returns the variable path in the format of "${path}"
        """

        return "${" + self.path + "}"

    @staticmethod
    def from_path(path: str) -> "Variable":
        """
        Create a variable from a given path.

        Example:

        .. code-block:: python

            Variable.from_path("var.my_variable")
        """

        return Variable(path=path, type=Any)


VariableOr = Union[Variable[T], T]
VariableOrOptional = Union[Variable[T], Optional[T]]

# - 1. variable: ${var.my_list}
# - 2. regular list: [{"name": "abc"}, ...]
# - 3. list of variables: ["${var.my_item}", ...]
# - 4. list with a mix of (3) and (4) as elements
VariableOrList = VariableOr[list[VariableOr[T]]]

# - 1. variable: ${var.my_list}
# - 2. regular dict: {"key": "value", ...}
# - 3. dict with variables (but not as keys): {"value": "${var.my_item}", ...}
# - 4. dict with a mix of (3) and (4) as values
VariableOrDict = VariableOr[dict[str, VariableOr[T]]]


def resolve_variable(value: VariableOr[T]) -> T:
    """
    Convenience method to resolve variable values. If the value is a variable,
    it will be resolved using :attr:`Variable.get` and returned. Otherwise,
    the value will be returned as is.
    """

    if value is None:
        # value is None, implies that T can be None
        return None  # type:ignore

    if isinstance(value, Variable):
        return value.get()

    return value


def resolve_variable_or_list(value: VariableOrList[T]) -> list[T]:
    """
    Convenience method to resolve variable values. If the value is a variable,
    or the list item is a variable, it will be resolved using :attr:`Variable.get`,
    and returned. Otherwise, the value will be returned as is.
    """

    return [resolve_variable(item) for item in resolve_variable(value)]


class Bundle:
    """
    Collection of variables for a bundle.
    """

    class Variables:
        """
        Access bundle variables. See :meth:`@variables <variables>` for declaring set of
        bundle variables statically.

        Example:
            .. code-block:: python

                Bundle.variables.warehouse_id # "${var.warehouse_id}"

        """

        def __getitem__(self, key) -> Variable:
            return Variable(path=f"{VAR_PREFIX}.{key}", type=Any)

        def __getattr__(self, item) -> Variable:
            return Variable(path=f"{VAR_PREFIX}.{item}", type=Any)

    class Workspace:
        class CurrentUser:
            # note: intentionally renamed from "userName" to "user_name"
            user_name: Variable[str] = Variable(
                path="workspace.current_user.userName",
                type=str,
            )
            """
            Example:
            
            .. code-block:: python
            
                @job(
                    email_notifications={
                        "on_failure": [Bundle.workspace.current_user.user_name],
                    },
                )
                def my_job():
                    ...
                    
            """

        current_user: CurrentUser = CurrentUser()
        """
        :meta hide-value:
        """

    workspace: Workspace = Workspace()
    """
    :meta hide-value:
    """

    variables: Variables = Variables()
    """
    :meta hide-value:
    """

    target: Variable[str] = Variable(path="bundle.target", type=str)
    """
    Deployment target for bundle.
    """

    environment: Variable[str] = Variable(path="bundle.environment", type=str)
    """
    Deprecated, use target instead.
    """


def variables(cls: type[T]) -> type[T]:
    """
    A decorator that initializes each annotated attribute in a class
    with :class:`~Variable` type. Variables are initialized with a path
    that corresponds to the attribute name. Variables should specify their
    type, or else they will be treated as :class:`~Any`. Complex types
    like data classes, lists or dictionaries are supported.

    For example, if your databricks.yml file contains:

    .. code-block:: yaml

        variables:
          warehouse_id:
            description: Warehouse ID for SQL tasks
            default: ...

    You can define a class with a `warehouse_id` attribute:

    .. code-block:: python

        @variables
        class MyVariables:
          warehouse_id: Variable[str] # ${var.warehouse_id}

    And later use it in your code as `MyVariables.warehouse_id`.

    For accessing bundle variable values, see :meth:`Variable.get`.
    """

    # making class a dataclass, solves a lot of problems, because we can just use 'fields'
    cls = dataclass(cls)
    assert is_dataclass(cls)

    # don't get type hints unless needed
    hints = None

    for field in fields(cls):
        field_type = field.type

        if isinstance(field_type, typing.ForwardRef) or isinstance(field_type, str):
            if hints is None:
                hints = typing.get_type_hints(cls)

            field_type = hints.get(field.name, field.type)

        origin = get_origin(field_type) or field_type

        if origin != Variable:
            raise ValueError(
                f"Only 'Variable' type is allowed in classes annotated with @variables, got {field_type}"
            )

        args = get_args(field_type)

        if not args:
            variable_type = Any
        else:
            variable_type = args[0]

        variable = Variable(path=f"var.{field.name}", type=variable_type)

        setattr(cls, field.name, variable)

    return cls


@dataclass(kw_only=True)
class VariableContext:
    """
    A context manager that allows to resolve variable values.

    :meta private: reserved for internal use, use :func:`Variable.get` instead.
    """

    _values: dict[str, Any]

    _STACK: ClassVar[list["Self"]] = []

    @staticmethod
    def get(variable: Variable[T]) -> T:
        if not VariableContext._STACK:
            raise ValueError(
                "Can't resolve variable values, are you calling '.get()' "
                "within @job, @resource_generator or @job_mutator?"
            )

        if not variable.path.startswith(VAR_PREFIX + "."):
            raise ValueError(
                "You can only get values of variables starting with 'var.*'"
            )
        else:
            variable_name = variable.path[len(VAR_PREFIX + ".") :]

        def _get_value():
            for frame in reversed(VariableContext._STACK):
                if variable_name in frame._values:
                    return frame._values[variable_name]

            raise ValueError(
                f"Can't find '{variable_name}' variable. Did you define it in databricks.yml?"
            )

        value = _get_value()

        # avoid circular import
        from databricks.bundles.internal._transform import (
            _display_type,
            _find_union_arg,
            _transform,
            _unwrap_variable_path,
        )

        if nested := _unwrap_variable_path(value):
            can_be_variable = get_origin(variable.type) == Union and _find_union_arg(
                nested, variable.type
            )
            can_be_variable = can_be_variable or get_origin(variable.type) == Variable

            if not can_be_variable:
                display_type = _display_type(variable.type)

                raise ValueError(
                    f"Failed to resolve '{variable_name}' because refers to another "
                    f"variable '{nested}'. Change variable type to "
                    f"Variable[VariableOr[{display_type}]]"
                )

        if variable.type == Any:
            return value

        try:
            return _transform(variable.type, value)
        except Exception as e:
            raise ValueError(f"Failed to read '{variable_name}' variable value") from e

    @staticmethod
    @contextmanager
    def push(values: dict[str, Any]):
        try:
            VariableContext._STACK.append(VariableContext(_values=values))
            yield
        finally:
            VariableContext._STACK.pop()
