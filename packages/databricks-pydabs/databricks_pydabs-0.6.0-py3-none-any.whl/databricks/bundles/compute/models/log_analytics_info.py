from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["LogAnalyticsInfo", "LogAnalyticsInfoParam"]


@dataclass(kw_only=True)
class LogAnalyticsInfo:
    """"""

    log_analytics_primary_key: VariableOrOptional[str] = None
    """
    <needs content added>
    """

    log_analytics_workspace_id: VariableOrOptional[str] = None
    """
    <needs content added>
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        log_analytics_primary_key: VariableOrOptional[str] = None,
        log_analytics_workspace_id: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class LogAnalyticsInfoDict(TypedDict, total=False):
    """"""

    log_analytics_primary_key: VariableOrOptional[str]
    """
    <needs content added>
    """

    log_analytics_workspace_id: VariableOrOptional[str]
    """
    <needs content added>
    """


LogAnalyticsInfoParam = LogAnalyticsInfoDict | LogAnalyticsInfo
