from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "ConditionTaskOp",
    "ConditionTaskOpParam",
    "ConditionTask",
    "ConditionTaskParam",
]


class ConditionTaskOp(Enum):
    EQUAL_TO = "EQUAL_TO"
    GREATER_THAN = "GREATER_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN = "LESS_THAN"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"
    NOT_EQUAL = "NOT_EQUAL"


ConditionTaskOpParam = (
    Literal[
        "EQUAL_TO",
        "GREATER_THAN",
        "GREATER_THAN_OR_EQUAL",
        "LESS_THAN",
        "LESS_THAN_OR_EQUAL",
        "NOT_EQUAL",
    ]
    | ConditionTaskOp
)


@dataclass(kw_only=True)
class ConditionTask:
    """"""

    left: VariableOr[str]
    """
    The left operand of the condition task. Can be either a string value or a job state or parameter reference.
    """

    op: VariableOr[ConditionTaskOp]
    """
    * `EQUAL_TO`, `NOT_EQUAL` operators perform string comparison of their operands. This means that `“12.0” == “12”` will evaluate to `false`.
    * `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`, `LESS_THAN`, `LESS_THAN_OR_EQUAL` operators perform numeric comparison of their operands. `“12.0” >= “12”` will evaluate to `true`, `“10.0” >= “12”` will evaluate to `false`.
    
    The boolean comparison to task values can be implemented with operators `EQUAL_TO`, `NOT_EQUAL`. If a task value was set to a boolean value, it will be serialized to `“true”` or `“false”` for the comparison.
    """

    right: VariableOr[str]
    """
    The right operand of the condition task. Can be either a string value or a job state or parameter reference.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        left: VariableOr[str],
        op: VariableOr[ConditionTaskOpParam],
        right: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class ConditionTaskDict(TypedDict, total=False):
    """"""

    left: VariableOr[str]
    """
    The left operand of the condition task. Can be either a string value or a job state or parameter reference.
    """

    op: VariableOr[ConditionTaskOpParam]
    """
    * `EQUAL_TO`, `NOT_EQUAL` operators perform string comparison of their operands. This means that `“12.0” == “12”` will evaluate to `false`.
    * `GREATER_THAN`, `GREATER_THAN_OR_EQUAL`, `LESS_THAN`, `LESS_THAN_OR_EQUAL` operators perform numeric comparison of their operands. `“12.0” >= “12”` will evaluate to `true`, `“10.0” >= “12”` will evaluate to `false`.
    
    The boolean comparison to task values can be implemented with operators `EQUAL_TO`, `NOT_EQUAL`. If a task value was set to a boolean value, it will be serialized to `“true”` or `“false”` for the comparison.
    """

    right: VariableOr[str]
    """
    The right operand of the condition task. Can be either a string value or a job state or parameter reference.
    """


ConditionTaskParam = ConditionTaskDict | ConditionTask
