from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.cron_schedule import CronSchedule, CronScheduleParam
from databricks.bundles.jobs.models.email_notifications import (
    JobEmailNotifications,
    JobEmailNotificationsParam,
    JobNotificationSettings,
    JobNotificationSettingsParam,
)
from databricks.bundles.jobs.models.git_source import GitSource, GitSourceParam
from databricks.bundles.jobs.models.job_cluster import JobCluster, JobClusterParam
from databricks.bundles.jobs.models.job_environment import (
    JobEnvironment,
    JobEnvironmentParam,
)
from databricks.bundles.jobs.models.job_parameter import (
    JobParameterDefinition,
    JobParameterDefinitionParam,
)
from databricks.bundles.jobs.models.job_run_as import JobRunAs, JobRunAsParam
from databricks.bundles.jobs.models.jobs_health import (
    JobsHealthRules,
    JobsHealthRulesParam,
)
from databricks.bundles.jobs.models.permission import Permission, PermissionParam
from databricks.bundles.jobs.models.queue_settings import (
    QueueSettings,
    QueueSettingsParam,
)
from databricks.bundles.jobs.models.task import Task, TaskParam
from databricks.bundles.jobs.models.trigger import (
    Continuous,
    ContinuousParam,
    TriggerSettings,
    TriggerSettingsParam,
)
from databricks.bundles.jobs.models.webhook_notifications import (
    WebhookNotifications,
    WebhookNotificationsParam,
)
from databricks.bundles.resource import Resource
from databricks.bundles.variables import (
    VariableOrDict,
    VariableOrList,
    VariableOrOptional,
)

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["Job", "JobParam"]


@dataclass(kw_only=True)
class Job(Resource):
    """"""

    continuous: VariableOrOptional[Continuous] = None
    """
    An optional continuous property for this job. The continuous property will ensure that there is always one run executing. Only one of `schedule` and `continuous` can be used.
    """

    description: VariableOrOptional[str] = None
    """
    An optional description for the job. The maximum length is 27700 characters in UTF-8 encoding.
    """

    email_notifications: VariableOrOptional[JobEmailNotifications] = None
    """
    An optional set of email addresses that is notified when runs of this job begin or complete as well as when this job is deleted.
    """

    environments: VariableOrList[JobEnvironment] = field(default_factory=list)
    """
    A list of task execution environment specifications that can be referenced by tasks of this job.
    """

    git_source: VariableOrOptional[GitSource] = None
    """
    An optional specification for a remote Git repository containing the source code used by tasks. Version-controlled source code is supported by notebook, dbt, Python script, and SQL File tasks.
    
    If `git_source` is set, these tasks retrieve the file from the remote repository by default. However, this behavior can be overridden by setting `source` to `WORKSPACE` on the task.
    
    Note: dbt and SQL File tasks support only version-controlled sources. If dbt or SQL File tasks are used, `git_source` must be defined on the job.
    """

    health: VariableOrOptional[JobsHealthRules] = None

    job_clusters: VariableOrList[JobCluster] = field(default_factory=list)
    """
    A list of job cluster specifications that can be shared and reused by tasks of this job. Libraries cannot be declared in a shared job cluster. You must declare dependent libraries in task settings.
    """

    max_concurrent_runs: VariableOrOptional[int] = None
    """
    An optional maximum allowed number of concurrent runs of the job.
    Set this value if you want to be able to execute multiple runs of the same job concurrently.
    This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters.
    This setting affects only new runs. For example, suppose the job’s concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won’t kill any of the active runs.
    However, from then on, new runs are skipped unless there are fewer than 3 active runs.
    This value cannot exceed 1000. Setting this value to `0` causes all new runs to be skipped.
    """

    name: VariableOrOptional[str] = None
    """
    An optional name for the job. The maximum length is 4096 bytes in UTF-8 encoding.
    """

    notification_settings: VariableOrOptional[JobNotificationSettings] = None
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this job.
    """

    parameters: VariableOrList[JobParameterDefinition] = field(default_factory=list)
    """
    Job-level parameter definitions
    """

    permissions: VariableOrList[Permission] = field(default_factory=list)

    queue: VariableOrOptional[QueueSettings] = None
    """
    The queue settings of the job.
    """

    run_as: VariableOrOptional[JobRunAs] = None

    schedule: VariableOrOptional[CronSchedule] = None
    """
    An optional periodic schedule for this job. The default behavior is that the job only runs when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    tags: VariableOrDict[str] = field(default_factory=dict)
    """
    A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
    """

    tasks: VariableOrList[Task] = field(default_factory=list)
    """
    A list of task specifications to be executed by this job.
    """

    timeout_seconds: VariableOrOptional[int] = None
    """
    An optional timeout applied to each run of this job. A value of `0` means no timeout.
    """

    trigger: VariableOrOptional[TriggerSettings] = None
    """
    A configuration to trigger a run when certain conditions are met. The default behavior is that the job runs only when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    webhook_notifications: VariableOrOptional[WebhookNotifications] = None
    """
    A collection of system notification IDs to notify when runs of this job begin or complete.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        resource_name: str,
        continuous: VariableOrOptional[ContinuousParam] = None,
        description: VariableOrOptional[str] = None,
        email_notifications: VariableOrOptional[JobEmailNotificationsParam] = None,
        environments: Optional[VariableOrList[JobEnvironmentParam]] = None,
        git_source: VariableOrOptional[GitSourceParam] = None,
        health: VariableOrOptional[JobsHealthRulesParam] = None,
        job_clusters: Optional[VariableOrList[JobClusterParam]] = None,
        max_concurrent_runs: VariableOrOptional[int] = None,
        name: VariableOrOptional[str] = None,
        notification_settings: VariableOrOptional[JobNotificationSettingsParam] = None,
        parameters: Optional[VariableOrList[JobParameterDefinitionParam]] = None,
        permissions: Optional[VariableOrList[PermissionParam]] = None,
        queue: VariableOrOptional[QueueSettingsParam] = None,
        run_as: VariableOrOptional[JobRunAsParam] = None,
        schedule: VariableOrOptional[CronScheduleParam] = None,
        tags: Optional[VariableOrDict[str]] = None,
        tasks: Optional[VariableOrList[TaskParam]] = None,
        timeout_seconds: VariableOrOptional[int] = None,
        trigger: VariableOrOptional[TriggerSettingsParam] = None,
        webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobDict(TypedDict, total=False):
    """"""

    continuous: VariableOrOptional[ContinuousParam]
    """
    An optional continuous property for this job. The continuous property will ensure that there is always one run executing. Only one of `schedule` and `continuous` can be used.
    """

    description: VariableOrOptional[str]
    """
    An optional description for the job. The maximum length is 27700 characters in UTF-8 encoding.
    """

    email_notifications: VariableOrOptional[JobEmailNotificationsParam]
    """
    An optional set of email addresses that is notified when runs of this job begin or complete as well as when this job is deleted.
    """

    environments: VariableOrList[JobEnvironmentParam]
    """
    A list of task execution environment specifications that can be referenced by tasks of this job.
    """

    git_source: VariableOrOptional[GitSourceParam]
    """
    An optional specification for a remote Git repository containing the source code used by tasks. Version-controlled source code is supported by notebook, dbt, Python script, and SQL File tasks.
    
    If `git_source` is set, these tasks retrieve the file from the remote repository by default. However, this behavior can be overridden by setting `source` to `WORKSPACE` on the task.
    
    Note: dbt and SQL File tasks support only version-controlled sources. If dbt or SQL File tasks are used, `git_source` must be defined on the job.
    """

    health: VariableOrOptional[JobsHealthRulesParam]

    job_clusters: VariableOrList[JobClusterParam]
    """
    A list of job cluster specifications that can be shared and reused by tasks of this job. Libraries cannot be declared in a shared job cluster. You must declare dependent libraries in task settings.
    """

    max_concurrent_runs: VariableOrOptional[int]
    """
    An optional maximum allowed number of concurrent runs of the job.
    Set this value if you want to be able to execute multiple runs of the same job concurrently.
    This is useful for example if you trigger your job on a frequent schedule and want to allow consecutive runs to overlap with each other, or if you want to trigger multiple runs which differ by their input parameters.
    This setting affects only new runs. For example, suppose the job’s concurrency is 4 and there are 4 concurrent active runs. Then setting the concurrency to 3 won’t kill any of the active runs.
    However, from then on, new runs are skipped unless there are fewer than 3 active runs.
    This value cannot exceed 1000. Setting this value to `0` causes all new runs to be skipped.
    """

    name: VariableOrOptional[str]
    """
    An optional name for the job. The maximum length is 4096 bytes in UTF-8 encoding.
    """

    notification_settings: VariableOrOptional[JobNotificationSettingsParam]
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this job.
    """

    parameters: VariableOrList[JobParameterDefinitionParam]
    """
    Job-level parameter definitions
    """

    permissions: VariableOrList[PermissionParam]

    queue: VariableOrOptional[QueueSettingsParam]
    """
    The queue settings of the job.
    """

    run_as: VariableOrOptional[JobRunAsParam]

    schedule: VariableOrOptional[CronScheduleParam]
    """
    An optional periodic schedule for this job. The default behavior is that the job only runs when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    tags: VariableOrDict[str]
    """
    A map of tags associated with the job. These are forwarded to the cluster as cluster tags for jobs clusters, and are subject to the same limitations as cluster tags. A maximum of 25 tags can be added to the job.
    """

    tasks: VariableOrList[TaskParam]
    """
    A list of task specifications to be executed by this job.
    """

    timeout_seconds: VariableOrOptional[int]
    """
    An optional timeout applied to each run of this job. A value of `0` means no timeout.
    """

    trigger: VariableOrOptional[TriggerSettingsParam]
    """
    A configuration to trigger a run when certain conditions are met. The default behavior is that the job runs only when triggered by clicking “Run Now” in the Jobs UI or sending an API request to `runNow`.
    """

    webhook_notifications: VariableOrOptional[WebhookNotificationsParam]
    """
    A collection of system notification IDs to notify when runs of this job begin or complete.
    """


JobParam = JobDict | Job
