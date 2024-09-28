from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "JobEmailNotifications",
    "JobEmailNotificationsParam",
    "TaskEmailNotifications",
    "TaskEmailNotificationsParam",
    "TaskNotificationSettings",
    "TaskNotificationSettingsParam",
    "JobNotificationSettings",
    "JobNotificationSettingsParam",
]


@dataclass(kw_only=True)
class JobEmailNotifications:
    """"""

    no_alert_for_skipped_runs: VariableOrOptional[bool] = None
    """
    If true, do not send email to recipients specified in `on_failure` if the run is skipped.
    """

    on_duration_warning_threshold_exceeded: VariableOrList[str] = field(
        default_factory=list
    )
    """
    A list of email addresses to be notified when the duration of a run exceeds the threshold specified for the `RUN_DURATION_SECONDS` metric in the `health` field. If no rule for the `RUN_DURATION_SECONDS` metric is specified in the `health` field for the job, notifications are not sent.
    """

    on_failure: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run unsuccessfully completes. A run is considered to have completed unsuccessfully if it ends with an `INTERNAL_ERROR` `life_cycle_state` or a `FAILED`, or `TIMED_OUT` result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.
    """

    on_start: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run begins. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    on_streaming_backlog_exceeded: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to notify when any streaming backlog thresholds are exceeded for any stream.
    Streaming backlog thresholds can be set in the `health` field using the following metrics: `STREAMING_BACKLOG_BYTES`, `STREAMING_BACKLOG_RECORDS`, `STREAMING_BACKLOG_SECONDS`, or `STREAMING_BACKLOG_FILES`.
    Alerting is based on the 10-minute average of these metrics. If the issue persists, notifications are resent every 30 minutes.
    """

    on_success: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run successfully completes. A run is considered to have completed successfully if it ends with a `TERMINATED` `life_cycle_state` and a `SUCCESS` result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        no_alert_for_skipped_runs: VariableOrOptional[bool] = None,
        on_duration_warning_threshold_exceeded: Optional[VariableOrList[str]] = None,
        on_failure: Optional[VariableOrList[str]] = None,
        on_start: Optional[VariableOrList[str]] = None,
        on_streaming_backlog_exceeded: Optional[VariableOrList[str]] = None,
        on_success: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobEmailNotificationsDict(TypedDict, total=False):
    """"""

    no_alert_for_skipped_runs: VariableOrOptional[bool]
    """
    If true, do not send email to recipients specified in `on_failure` if the run is skipped.
    """

    on_duration_warning_threshold_exceeded: VariableOrList[str]
    """
    A list of email addresses to be notified when the duration of a run exceeds the threshold specified for the `RUN_DURATION_SECONDS` metric in the `health` field. If no rule for the `RUN_DURATION_SECONDS` metric is specified in the `health` field for the job, notifications are not sent.
    """

    on_failure: VariableOrList[str]
    """
    A list of email addresses to be notified when a run unsuccessfully completes. A run is considered to have completed unsuccessfully if it ends with an `INTERNAL_ERROR` `life_cycle_state` or a `FAILED`, or `TIMED_OUT` result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.
    """

    on_start: VariableOrList[str]
    """
    A list of email addresses to be notified when a run begins. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    on_streaming_backlog_exceeded: VariableOrList[str]
    """
    A list of email addresses to notify when any streaming backlog thresholds are exceeded for any stream.
    Streaming backlog thresholds can be set in the `health` field using the following metrics: `STREAMING_BACKLOG_BYTES`, `STREAMING_BACKLOG_RECORDS`, `STREAMING_BACKLOG_SECONDS`, or `STREAMING_BACKLOG_FILES`.
    Alerting is based on the 10-minute average of these metrics. If the issue persists, notifications are resent every 30 minutes.
    """

    on_success: VariableOrList[str]
    """
    A list of email addresses to be notified when a run successfully completes. A run is considered to have completed successfully if it ends with a `TERMINATED` `life_cycle_state` and a `SUCCESS` result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """


JobEmailNotificationsParam = JobEmailNotificationsDict | JobEmailNotifications


@dataclass(kw_only=True)
class TaskEmailNotifications:
    """"""

    no_alert_for_skipped_runs: VariableOrOptional[bool] = None
    """
    If true, do not send email to recipients specified in `on_failure` if the run is skipped.
    """

    on_duration_warning_threshold_exceeded: VariableOrList[str] = field(
        default_factory=list
    )
    """
    A list of email addresses to be notified when the duration of a run exceeds the threshold specified for the `RUN_DURATION_SECONDS` metric in the `health` field. If no rule for the `RUN_DURATION_SECONDS` metric is specified in the `health` field for the job, notifications are not sent.
    """

    on_failure: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run unsuccessfully completes. A run is considered to have completed unsuccessfully if it ends with an `INTERNAL_ERROR` `life_cycle_state` or a `FAILED`, or `TIMED_OUT` result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.
    """

    on_start: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run begins. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    on_streaming_backlog_exceeded: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to notify when any streaming backlog thresholds are exceeded for any stream.
    Streaming backlog thresholds can be set in the `health` field using the following metrics: `STREAMING_BACKLOG_BYTES`, `STREAMING_BACKLOG_RECORDS`, `STREAMING_BACKLOG_SECONDS`, or `STREAMING_BACKLOG_FILES`.
    Alerting is based on the 10-minute average of these metrics. If the issue persists, notifications are resent every 30 minutes.
    """

    on_success: VariableOrList[str] = field(default_factory=list)
    """
    A list of email addresses to be notified when a run successfully completes. A run is considered to have completed successfully if it ends with a `TERMINATED` `life_cycle_state` and a `SUCCESS` result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        no_alert_for_skipped_runs: VariableOrOptional[bool] = None,
        on_duration_warning_threshold_exceeded: Optional[VariableOrList[str]] = None,
        on_failure: Optional[VariableOrList[str]] = None,
        on_start: Optional[VariableOrList[str]] = None,
        on_streaming_backlog_exceeded: Optional[VariableOrList[str]] = None,
        on_success: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TaskEmailNotificationsDict(TypedDict, total=False):
    """"""

    no_alert_for_skipped_runs: VariableOrOptional[bool]
    """
    If true, do not send email to recipients specified in `on_failure` if the run is skipped.
    """

    on_duration_warning_threshold_exceeded: VariableOrList[str]
    """
    A list of email addresses to be notified when the duration of a run exceeds the threshold specified for the `RUN_DURATION_SECONDS` metric in the `health` field. If no rule for the `RUN_DURATION_SECONDS` metric is specified in the `health` field for the job, notifications are not sent.
    """

    on_failure: VariableOrList[str]
    """
    A list of email addresses to be notified when a run unsuccessfully completes. A run is considered to have completed unsuccessfully if it ends with an `INTERNAL_ERROR` `life_cycle_state` or a `FAILED`, or `TIMED_OUT` result_state. If this is not specified on job creation, reset, or update the list is empty, and notifications are not sent.
    """

    on_start: VariableOrList[str]
    """
    A list of email addresses to be notified when a run begins. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """

    on_streaming_backlog_exceeded: VariableOrList[str]
    """
    A list of email addresses to notify when any streaming backlog thresholds are exceeded for any stream.
    Streaming backlog thresholds can be set in the `health` field using the following metrics: `STREAMING_BACKLOG_BYTES`, `STREAMING_BACKLOG_RECORDS`, `STREAMING_BACKLOG_SECONDS`, or `STREAMING_BACKLOG_FILES`.
    Alerting is based on the 10-minute average of these metrics. If the issue persists, notifications are resent every 30 minutes.
    """

    on_success: VariableOrList[str]
    """
    A list of email addresses to be notified when a run successfully completes. A run is considered to have completed successfully if it ends with a `TERMINATED` `life_cycle_state` and a `SUCCESS` result_state. If not specified on job creation, reset, or update, the list is empty, and notifications are not sent.
    """


TaskEmailNotificationsParam = TaskEmailNotificationsDict | TaskEmailNotifications


@dataclass(kw_only=True)
class TaskNotificationSettings:
    """"""

    alert_on_last_attempt: VariableOrOptional[bool] = None
    """
    If true, do not send notifications to recipients specified in `on_start` for the retried runs and do not send notifications to recipients specified in `on_failure` until the last retry of the run.
    """

    no_alert_for_canceled_runs: VariableOrOptional[bool] = None
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is canceled.
    """

    no_alert_for_skipped_runs: VariableOrOptional[bool] = None
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is skipped.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        alert_on_last_attempt: VariableOrOptional[bool] = None,
        no_alert_for_canceled_runs: VariableOrOptional[bool] = None,
        no_alert_for_skipped_runs: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TaskNotificationSettingsDict(TypedDict, total=False):
    """"""

    alert_on_last_attempt: VariableOrOptional[bool]
    """
    If true, do not send notifications to recipients specified in `on_start` for the retried runs and do not send notifications to recipients specified in `on_failure` until the last retry of the run.
    """

    no_alert_for_canceled_runs: VariableOrOptional[bool]
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is canceled.
    """

    no_alert_for_skipped_runs: VariableOrOptional[bool]
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is skipped.
    """


TaskNotificationSettingsParam = TaskNotificationSettingsDict | TaskNotificationSettings


@dataclass(kw_only=True)
class JobNotificationSettings:
    """"""

    no_alert_for_canceled_runs: VariableOrOptional[bool] = None
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is canceled.
    """

    no_alert_for_skipped_runs: VariableOrOptional[bool] = None
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is skipped.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        no_alert_for_canceled_runs: VariableOrOptional[bool] = None,
        no_alert_for_skipped_runs: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobNotificationSettingsDict(TypedDict, total=False):
    """"""

    no_alert_for_canceled_runs: VariableOrOptional[bool]
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is canceled.
    """

    no_alert_for_skipped_runs: VariableOrOptional[bool]
    """
    If true, do not send notifications to recipients specified in `on_failure` if the run is skipped.
    """


JobNotificationSettingsParam = JobNotificationSettingsDict | JobNotificationSettings
