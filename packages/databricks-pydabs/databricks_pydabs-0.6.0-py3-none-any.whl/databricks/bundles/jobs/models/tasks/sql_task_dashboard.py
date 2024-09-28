from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.tasks.sql_task_subscription import (
    SqlTaskSubscription,
    SqlTaskSubscriptionParam,
)
from databricks.bundles.variables import VariableOr, VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTaskDashboard", "SqlTaskDashboardParam"]


@dataclass(kw_only=True)
class SqlTaskDashboard:
    """"""

    dashboard_id: VariableOr[str]
    """
    The canonical identifier of the SQL dashboard.
    """

    custom_subject: VariableOrOptional[str] = None
    """
    Subject of the email sent to subscribers of this task.
    """

    pause_subscriptions: VariableOrOptional[bool] = None
    """
    If true, the dashboard snapshot is not taken, and emails are not sent to subscribers.
    """

    subscriptions: VariableOrList[SqlTaskSubscription] = field(default_factory=list)
    """
    If specified, dashboard snapshots are sent to subscriptions.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        dashboard_id: VariableOr[str],
        custom_subject: VariableOrOptional[str] = None,
        pause_subscriptions: VariableOrOptional[bool] = None,
        subscriptions: Optional[VariableOrList[SqlTaskSubscriptionParam]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskDashboardDict(TypedDict, total=False):
    """"""

    dashboard_id: VariableOr[str]
    """
    The canonical identifier of the SQL dashboard.
    """

    custom_subject: VariableOrOptional[str]
    """
    Subject of the email sent to subscribers of this task.
    """

    pause_subscriptions: VariableOrOptional[bool]
    """
    If true, the dashboard snapshot is not taken, and emails are not sent to subscribers.
    """

    subscriptions: VariableOrList[SqlTaskSubscriptionParam]
    """
    If specified, dashboard snapshots are sent to subscriptions.
    """


SqlTaskDashboardParam = SqlTaskDashboardDict | SqlTaskDashboard
