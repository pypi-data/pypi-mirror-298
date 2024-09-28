from dataclasses import dataclass, field
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.pause_status import PauseStatus, PauseStatusParam
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["CronSchedule", "CronScheduleParam"]


@dataclass
class CronSchedule:
    """"""

    quartz_cron_expression: VariableOr[str]
    """
    A Cron expression using Quartz syntax that describes the schedule for a job. See [Cron Trigger](http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html) for details. This field is required.
    """

    timezone_id: VariableOr[str] = field(default="UTC", kw_only=True)
    """
    A Java timezone ID. The schedule for a job is resolved with respect to this timezone. See [Java TimeZone](https://docs.oracle.com/javase/7/docs/api/java/util/TimeZone.html) for details. This field is required.
    """

    pause_status: VariableOrOptional[PauseStatus] = field(default=None, kw_only=True)
    """
    Indicate whether this schedule is paused or not.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        quartz_cron_expression: VariableOr[str],
        timezone_id: VariableOr[str] = "UTC",
        pause_status: VariableOrOptional[PauseStatusParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class CronScheduleDict(TypedDict, total=False):
    """"""

    quartz_cron_expression: VariableOr[str]
    """
    A Cron expression using Quartz syntax that describes the schedule for a job. See [Cron Trigger](http://www.quartz-scheduler.org/documentation/quartz-2.3.0/tutorials/crontrigger.html) for details. This field is required.
    """

    timezone_id: VariableOr[str]
    """
    A Java timezone ID. The schedule for a job is resolved with respect to this timezone. See [Java TimeZone](https://docs.oracle.com/javase/7/docs/api/java/util/TimeZone.html) for details. This field is required.
    """

    pause_status: VariableOrOptional[PauseStatusParam]
    """
    Indicate whether this schedule is paused or not.
    """


CronScheduleParam = CronScheduleDict | CronSchedule
