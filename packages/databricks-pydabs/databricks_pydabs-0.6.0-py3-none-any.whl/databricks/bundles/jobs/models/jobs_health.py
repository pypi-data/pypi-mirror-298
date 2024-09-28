from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "JobsHealthOperator",
    "JobsHealthOperatorParam",
    "JobsHealthMetric",
    "JobsHealthMetricParam",
    "JobsHealthRule",
    "JobsHealthRuleParam",
    "JobsHealthRules",
    "JobsHealthRulesParam",
]


class JobsHealthOperator(Enum):
    GREATER_THAN = "GREATER_THAN"


JobsHealthOperatorParam = Literal["GREATER_THAN"] | JobsHealthOperator


class JobsHealthMetric(Enum):
    RUN_DURATION_SECONDS = "RUN_DURATION_SECONDS"
    STREAMING_BACKLOG_BYTES = "STREAMING_BACKLOG_BYTES"
    STREAMING_BACKLOG_RECORDS = "STREAMING_BACKLOG_RECORDS"
    STREAMING_BACKLOG_SECONDS = "STREAMING_BACKLOG_SECONDS"
    STREAMING_BACKLOG_FILES = "STREAMING_BACKLOG_FILES"


JobsHealthMetricParam = (
    Literal[
        "RUN_DURATION_SECONDS",
        "STREAMING_BACKLOG_BYTES",
        "STREAMING_BACKLOG_RECORDS",
        "STREAMING_BACKLOG_SECONDS",
        "STREAMING_BACKLOG_FILES",
    ]
    | JobsHealthMetric
)


@dataclass(kw_only=True)
class JobsHealthRule:
    """"""

    metric: VariableOr[JobsHealthMetric]

    op: VariableOr[JobsHealthOperator]

    value: VariableOr[int]
    """
    Specifies the threshold value that the health metric should obey to satisfy the health rule.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        metric: VariableOr[JobsHealthMetricParam],
        op: VariableOr[JobsHealthOperatorParam],
        value: VariableOr[int],
    ) -> "Self":
        return _transform(cls, locals())


class JobsHealthRuleDict(TypedDict, total=False):
    """"""

    metric: VariableOr[JobsHealthMetricParam]

    op: VariableOr[JobsHealthOperatorParam]

    value: VariableOr[int]
    """
    Specifies the threshold value that the health metric should obey to satisfy the health rule.
    """


JobsHealthRuleParam = JobsHealthRuleDict | JobsHealthRule


@dataclass(kw_only=True)
class JobsHealthRules:
    """"""

    rules: VariableOrList[JobsHealthRule] = field(default_factory=list)

    @classmethod
    def create(
        cls,
        /,
        *,
        rules: Optional[VariableOrList[JobsHealthRuleParam]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobsHealthRulesDict(TypedDict, total=False):
    """"""

    rules: VariableOrList[JobsHealthRuleParam]


JobsHealthRulesParam = JobsHealthRulesDict | JobsHealthRules
