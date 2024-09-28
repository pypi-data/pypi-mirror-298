from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.tasks.sql_task_subscription import (
    SqlTaskSubscription,
    SqlTaskSubscriptionParam,
)
from databricks.bundles.variables import VariableOr, VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTaskAlert", "SqlTaskAlertParam"]


@dataclass(kw_only=True)
class SqlTaskAlert:
    """"""

    alert_id: VariableOr[str]
    """
    The canonical identifier of the SQL alert.
    """

    subscriptions: VariableOrList[SqlTaskSubscription]
    """
    If specified, alert notifications are sent to subscribers.
    """

    pause_subscriptions: VariableOrOptional[bool] = None
    """
    If true, the alert notifications are not sent to subscribers.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        alert_id: VariableOr[str],
        subscriptions: VariableOrList[SqlTaskSubscriptionParam],
        pause_subscriptions: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskAlertDict(TypedDict, total=False):
    """"""

    alert_id: VariableOr[str]
    """
    The canonical identifier of the SQL alert.
    """

    subscriptions: VariableOrList[SqlTaskSubscriptionParam]
    """
    If specified, alert notifications are sent to subscribers.
    """

    pause_subscriptions: VariableOrOptional[bool]
    """
    If true, the alert notifications are not sent to subscribers.
    """


SqlTaskAlertParam = SqlTaskAlertDict | SqlTaskAlert
