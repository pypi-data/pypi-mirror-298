from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.tasks.sql_task_alert import (
    SqlTaskAlert,
    SqlTaskAlertParam,
)
from databricks.bundles.jobs.models.tasks.sql_task_dashboard import (
    SqlTaskDashboard,
    SqlTaskDashboardParam,
)
from databricks.bundles.jobs.models.tasks.sql_task_file import (
    SqlTaskFile,
    SqlTaskFileParam,
)
from databricks.bundles.jobs.models.tasks.sql_task_query import (
    SqlTaskQuery,
    SqlTaskQueryParam,
)
from databricks.bundles.variables import VariableOr, VariableOrDict, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTask", "SqlTaskParam"]


@dataclass(kw_only=True)
class SqlTask:
    """"""

    warehouse_id: VariableOr[str]
    """
    The canonical identifier of the SQL warehouse. Recommended to use with serverless or pro SQL warehouses. Classic SQL warehouses are only supported for SQL alert, dashboard and query tasks and are limited to scheduled single-task jobs.
    """

    alert: VariableOrOptional[SqlTaskAlert] = None
    """
    If alert, indicates that this job must refresh a SQL alert.
    """

    dashboard: VariableOrOptional[SqlTaskDashboard] = None
    """
    If dashboard, indicates that this job must refresh a SQL dashboard.
    """

    file: VariableOrOptional[SqlTaskFile] = None
    """
    If file, indicates that this job runs a SQL file in a remote Git repository.
    """

    parameters: VariableOrDict[str] = field(default_factory=dict)
    """
    Parameters to be used for each run of this job. The SQL alert task does not support custom parameters.
    """

    query: VariableOrOptional[SqlTaskQuery] = None
    """
    If query, indicates that this job must execute a SQL query.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        warehouse_id: VariableOr[str],
        alert: VariableOrOptional[SqlTaskAlertParam] = None,
        dashboard: VariableOrOptional[SqlTaskDashboardParam] = None,
        file: VariableOrOptional[SqlTaskFileParam] = None,
        parameters: Optional[VariableOrDict[str]] = None,
        query: VariableOrOptional[SqlTaskQueryParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskDict(TypedDict, total=False):
    """"""

    warehouse_id: VariableOr[str]
    """
    The canonical identifier of the SQL warehouse. Recommended to use with serverless or pro SQL warehouses. Classic SQL warehouses are only supported for SQL alert, dashboard and query tasks and are limited to scheduled single-task jobs.
    """

    alert: VariableOrOptional[SqlTaskAlertParam]
    """
    If alert, indicates that this job must refresh a SQL alert.
    """

    dashboard: VariableOrOptional[SqlTaskDashboardParam]
    """
    If dashboard, indicates that this job must refresh a SQL dashboard.
    """

    file: VariableOrOptional[SqlTaskFileParam]
    """
    If file, indicates that this job runs a SQL file in a remote Git repository.
    """

    parameters: VariableOrDict[str]
    """
    Parameters to be used for each run of this job. The SQL alert task does not support custom parameters.
    """

    query: VariableOrOptional[SqlTaskQueryParam]
    """
    If query, indicates that this job must execute a SQL query.
    """


SqlTaskParam = SqlTaskDict | SqlTask
