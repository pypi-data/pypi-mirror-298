from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from databricks.bundles.jobs.internal.inspections import Inspections

if TYPE_CHECKING:
    from typing_extensions import Self


@dataclass
class Signature:
    return_type: dict[str, type]
    parameters: dict[str, type]

    @classmethod
    def from_function(cls, function: Callable) -> "Self":
        return_type = Inspections.get_return_type(function)
        parameters = Inspections.get_parameters(function)

        return cls(
            return_type=return_type,
            parameters=parameters,
        )
