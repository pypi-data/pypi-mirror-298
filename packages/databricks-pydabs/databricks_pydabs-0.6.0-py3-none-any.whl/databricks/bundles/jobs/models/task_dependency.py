from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["TaskDependency", "TaskDependencyParam"]


@dataclass
class TaskDependency:
    """"""

    task_key: VariableOr[str]
    """
    The name of the task this task depends on.
    """

    outcome: VariableOrOptional[str] = field(default=None, kw_only=True)
    """
    Can only be specified on condition task dependencies. The outcome of the dependent task that must be met for this task to run.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        task_key: VariableOr[str],
        outcome: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TaskDependencyDict(TypedDict, total=False):
    """"""

    task_key: VariableOr[str]
    """
    The name of the task this task depends on.
    """

    outcome: VariableOrOptional[str]
    """
    Can only be specified on condition task dependencies. The outcome of the dependent task that must be met for this task to run.
    """


TaskDependencyParam = TaskDependencyDict | TaskDependency
