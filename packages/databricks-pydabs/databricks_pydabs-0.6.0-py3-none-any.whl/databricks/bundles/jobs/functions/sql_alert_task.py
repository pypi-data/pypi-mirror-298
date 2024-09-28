from dataclasses import dataclass
from enum import Enum

from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput

__all__ = [
    "AlertState",
    "SqlAlertTaskFunction",
    "SqlAlertTaskOutput",
    "SqlAlertTaskWithOutput",
]


class AlertState(Enum):
    """
    The state of the SQL alert.

    - UNKNOWN: alert yet to be evaluated
    - OK: alert evaluated and did not fulfill trigger conditions
    - TRIGGERED: alert evaluated and fulfilled trigger conditions
    """

    UNKNOWN = "UNKNOWN"
    OK = "OK"
    TRIGGERED = "TRIGGERED"


@dataclass(kw_only=True)
class SqlAlertTaskOutput:
    """
    The output of the SQL alert task.
    """

    alert_state: AlertState
    """
    The state of the SQL alert.
    """


@dataclass
class SqlAlertTaskWithOutput(TaskWithOutput):
    """
    SQL alert task with output.

    See also :meth:`~databricks.bundles.jobs.sql_alert_task`.
    """

    @property
    def output(self) -> SqlAlertTaskOutput:
        raise Exception(
            "Accessing task output outside of @job decorator isn't supported"
        )


@dataclass(frozen=True)
class SqlAlertTaskFunction(TaskFunction[[], None]):
    """
    Returns :class:`~databricks.bundles.jobs.functions.sql_alert_task.SqlAlertTaskWithOutput`
    when called within function annotated with :func:`@job <databricks.bundles.jobs.job>`.

    See also :meth:`~databricks.bundles.jobs.sql_alert_task`.
    """

    base_task: SqlAlertTaskWithOutput

    def __call__(self) -> SqlAlertTaskWithOutput:
        return super().__call__()  # type:ignore
