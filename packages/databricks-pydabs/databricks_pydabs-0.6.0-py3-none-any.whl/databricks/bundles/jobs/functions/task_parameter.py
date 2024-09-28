from dataclasses import dataclass
from typing import Any, Optional, Union

__all__ = [
    "ConstantParameter",
    "TaskReferenceParameter",
    "JobParameter",
    "TaskParameter",
]

from databricks.bundles.jobs.internal.parameters import _serialize_parameter
from databricks.bundles.variables import Variable


@dataclass(frozen=True)
class ConstantParameter:
    """
    Parameter where the value is a constant.

    :meta private: reserved for internal use
    """

    value: Any

    @property
    def value_type(self) -> type:
        return type(self.value)

    def serialize(self) -> str:
        return _serialize_parameter(type(self.value), self.value)


@dataclass(kw_only=True, frozen=True)
class TaskReferenceParameter:
    """
    Parameter where the value is a task value or output of another task.

    :meta private: reserved for internal use
    """

    task_key: str
    path: list[str]

    def serialize(self) -> str:
        return f"{{{{tasks.{self.task_key}.{'.'.join(self.path)}}}}}"

    def __post_init__(self):
        if not self.path:
            raise ValueError("Path must not be empty")


@dataclass(kw_only=True, frozen=True)
class ForEachInputTaskParameter:
    """
    Parameter where value is a reference to iteration variable in a for-each task.

    :meta private: reserved for internal use
    """

    attribute: Optional[str] = None

    def serialize(self) -> str:
        if self.attribute:
            return f"{{{{input.{self.attribute}}}}}"
        else:
            return "{{input}}"


@dataclass(kw_only=True, frozen=True)
class VariableParameter:
    """
    Parameter where value is a custom variable reference like ${var.task_parameter}.

    :meta private: reserved for internal use
    """

    variable: Variable

    def serialize(self) -> str:
        return self.variable.value


@dataclass(kw_only=True, frozen=True)
class JobParameter:
    """
    Job-level parameter.

    :meta private: reserved for internal use
    """

    name: str
    value_type: type
    default_value: Any

    def __post_init__(self):
        if not isinstance(self.default_value, self.value_type):
            raise ValueError(
                f"Expected default value for parameter '{self.name}' to be {self.value_type}, "
                f"but got {type(self.default_value)}"
            )

    def serialize(self) -> str:
        return f"{{{{job.parameters.{self.name}}}}}"


TaskParameter = Union[
    ConstantParameter,
    TaskReferenceParameter,
    JobParameter,
    ForEachInputTaskParameter,
    VariableParameter,
]
