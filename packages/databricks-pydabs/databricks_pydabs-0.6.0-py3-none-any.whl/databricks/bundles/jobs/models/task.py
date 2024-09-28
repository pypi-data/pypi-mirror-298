from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.compute.models.cluster_spec import ClusterSpec, ClusterSpecParam
from databricks.bundles.compute.models.library import Library, LibraryParam
from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.email_notifications import (
    TaskEmailNotifications,
    TaskEmailNotificationsParam,
    TaskNotificationSettings,
    TaskNotificationSettingsParam,
)
from databricks.bundles.jobs.models.jobs_health import (
    JobsHealthRules,
    JobsHealthRulesParam,
)
from databricks.bundles.jobs.models.run_if import RunIf, RunIfParam
from databricks.bundles.jobs.models.task_dependency import (
    TaskDependency,
    TaskDependencyParam,
)
from databricks.bundles.jobs.models.tasks.condition_task import (
    ConditionTask,
    ConditionTaskParam,
)
from databricks.bundles.jobs.models.tasks.dbt_task import DbtTask, DbtTaskParam
from databricks.bundles.jobs.models.tasks.for_each_task import (
    ForEachTask,
    ForEachTaskParam,
)
from databricks.bundles.jobs.models.tasks.notebook_task import (
    NotebookTask,
    NotebookTaskParam,
)
from databricks.bundles.jobs.models.tasks.pipeline_task import (
    PipelineTask,
    PipelineTaskParam,
)
from databricks.bundles.jobs.models.tasks.python_wheel_task import (
    PythonWheelTask,
    PythonWheelTaskParam,
)
from databricks.bundles.jobs.models.tasks.run_job_task import (
    RunJobTask,
    RunJobTaskParam,
)
from databricks.bundles.jobs.models.tasks.spark_jar_task import (
    SparkJarTask,
    SparkJarTaskParam,
)
from databricks.bundles.jobs.models.tasks.spark_python_task import (
    SparkPythonTask,
    SparkPythonTaskParam,
)
from databricks.bundles.jobs.models.tasks.spark_submit_task import (
    SparkSubmitTask,
    SparkSubmitTaskParam,
)
from databricks.bundles.jobs.models.tasks.sql_task import SqlTask, SqlTaskParam
from databricks.bundles.jobs.models.webhook_notifications import (
    WebhookNotifications,
    WebhookNotificationsParam,
)
from databricks.bundles.variables import VariableOr, VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["Task", "TaskParam"]


@dataclass(kw_only=True)
class Task:
    """"""

    task_key: VariableOr[str]
    """
    A unique name for the task. This field is used to refer to this task from other tasks.
    This field is required and must be unique within its parent job.
    On Update or Reset, this field is used to reference the tasks to be updated or reset.
    """

    condition_task: VariableOrOptional[ConditionTask] = None
    """
    If condition_task, specifies a condition with an outcome that can be used to control the execution of other tasks. Does not require a cluster to execute and does not support retries or notifications.
    """

    dbt_task: VariableOrOptional[DbtTask] = None
    """
    If dbt_task, indicates that this must execute a dbt task. It requires both Databricks SQL and the ability to use a serverless or a pro SQL warehouse.
    """

    depends_on: VariableOrList[TaskDependency] = field(default_factory=list)
    """
    An optional array of objects specifying the dependency graph of the task. All tasks specified in this field must complete before executing this task. The task will run only if the `run_if` condition is true.
    The key is `task_key`, and the value is the name assigned to the dependent task.
    """

    description: VariableOrOptional[str] = None
    """
    An optional description for this task.
    """

    disable_auto_optimization: VariableOrOptional[bool] = None
    """
    An option to disable auto optimization in serverless
    """

    email_notifications: VariableOrOptional[TaskEmailNotifications] = None
    """
    An optional set of email addresses that is notified when runs of this task begin or complete as well as when this task is deleted. The default behavior is to not send any emails.
    """

    environment_key: VariableOrOptional[str] = None
    """
    The key that references an environment spec in a job. This field is required for Python script, Python wheel and dbt tasks when using serverless compute.
    """

    existing_cluster_id: VariableOrOptional[str] = None
    """
    If existing_cluster_id, the ID of an existing cluster that is used for all runs.
    When running jobs or tasks on an existing cluster, you may need to manually restart
    the cluster if it stops responding. We suggest running jobs and tasks on new clusters for
    greater reliability
    """

    for_each_task: VariableOrOptional[ForEachTask] = None
    """
    If for_each_task, indicates that this task must execute the nested task within it.
    """

    health: VariableOrOptional[JobsHealthRules] = None

    job_cluster_key: VariableOrOptional[str] = None
    """
    If job_cluster_key, this task is executed reusing the cluster specified in `job.settings.job_clusters`.
    """

    libraries: VariableOrList[Library] = field(default_factory=list)
    """
    An optional list of libraries to be installed on the cluster.
    The default value is an empty list.
    """

    max_retries: VariableOrOptional[int] = None
    """
    An optional maximum number of times to retry an unsuccessful run. A run is considered to be unsuccessful if it completes with the `FAILED` result_state or `INTERNAL_ERROR` `life_cycle_state`. The value `-1` means to retry indefinitely and the value `0` means to never retry.
    """

    min_retry_interval_millis: VariableOrOptional[int] = None
    """
    An optional minimal interval in milliseconds between the start of the failed run and the subsequent retry run. The default behavior is that unsuccessful runs are immediately retried.
    """

    new_cluster: VariableOrOptional[ClusterSpec] = None
    """
    If new_cluster, a description of a new cluster that is created for each run.
    """

    notebook_task: VariableOrOptional[NotebookTask] = None
    """
    If notebook_task, indicates that this task must run a notebook. This field may not be specified in conjunction with spark_jar_task.
    """

    notification_settings: VariableOrOptional[TaskNotificationSettings] = None
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this task.
    """

    pipeline_task: VariableOrOptional[PipelineTask] = None
    """
    If pipeline_task, indicates that this task must execute a Pipeline.
    """

    python_wheel_task: VariableOrOptional[PythonWheelTask] = None
    """
    If python_wheel_task, indicates that this job must execute a PythonWheel.
    """

    retry_on_timeout: VariableOrOptional[bool] = None
    """
    An optional policy to specify whether to retry a job when it times out. The default behavior
    is to not retry on timeout.
    """

    run_if: VariableOrOptional[RunIf] = None
    """
    An optional value specifying the condition determining whether the task is run once its dependencies have been completed.
    
    * `ALL_SUCCESS`: All dependencies have executed and succeeded
    * `AT_LEAST_ONE_SUCCESS`: At least one dependency has succeeded
    * `NONE_FAILED`: None of the dependencies have failed and at least one was executed
    * `ALL_DONE`: All dependencies have been completed
    * `AT_LEAST_ONE_FAILED`: At least one dependency failed
    * `ALL_FAILED`: ALl dependencies have failed
    """

    run_job_task: VariableOrOptional[RunJobTask] = None
    """
    If run_job_task, indicates that this task must execute another job.
    """

    spark_jar_task: VariableOrOptional[SparkJarTask] = None
    """
    If spark_jar_task, indicates that this task must run a JAR.
    """

    spark_python_task: VariableOrOptional[SparkPythonTask] = None
    """
    If spark_python_task, indicates that this task must run a Python file.
    """

    spark_submit_task: VariableOrOptional[SparkSubmitTask] = None
    """
    If `spark_submit_task`, indicates that this task must be launched by the spark submit script. This task can run only on new clusters.
    
    In the `new_cluster` specification, `libraries` and `spark_conf` are not supported. Instead, use `--jars` and `--py-files` to add Java and Python libraries and `--conf` to set the Spark configurations.
    
    `master`, `deploy-mode`, and `executor-cores` are automatically configured by Databricks; you _cannot_ specify them in parameters.
    
    By default, the Spark submit job uses all available memory (excluding reserved memory for Databricks services). You can set `--driver-memory`, and `--executor-memory` to a smaller value to leave some room for off-heap usage.
    
    The `--jars`, `--py-files`, `--files` arguments support DBFS and S3 paths.
    """

    sql_task: VariableOrOptional[SqlTask] = None
    """
    If sql_task, indicates that this job must execute a SQL task.
    """

    timeout_seconds: VariableOrOptional[int] = None
    """
    An optional timeout applied to each run of this job task. A value of `0` means no timeout.
    """

    webhook_notifications: VariableOrOptional[WebhookNotifications] = None
    """
    A collection of system notification IDs to notify when runs of this task begin or complete. The default behavior is to not send any system notifications.
    """

    def __post_init__(self):
        union_fields = [
            self.new_cluster,
            self.job_cluster_key,
            self.environment_key,
            self.existing_cluster_id,
        ]

        if sum(f is not None for f in union_fields) > 1:
            raise ValueError(
                "Only one of 'new_cluster', 'job_cluster_key', 'environment_key', 'existing_cluster_id' can be specified in Task"
            )

    @classmethod
    def create(
        cls,
        /,
        *,
        task_key: VariableOr[str],
        condition_task: VariableOrOptional[ConditionTaskParam] = None,
        dbt_task: VariableOrOptional[DbtTaskParam] = None,
        depends_on: Optional[VariableOrList[TaskDependencyParam]] = None,
        description: VariableOrOptional[str] = None,
        disable_auto_optimization: VariableOrOptional[bool] = None,
        email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
        environment_key: VariableOrOptional[str] = None,
        existing_cluster_id: VariableOrOptional[str] = None,
        for_each_task: VariableOrOptional[ForEachTaskParam] = None,
        health: VariableOrOptional[JobsHealthRulesParam] = None,
        job_cluster_key: VariableOrOptional[str] = None,
        libraries: Optional[VariableOrList[LibraryParam]] = None,
        max_retries: VariableOrOptional[int] = None,
        min_retry_interval_millis: VariableOrOptional[int] = None,
        new_cluster: VariableOrOptional[ClusterSpecParam] = None,
        notebook_task: VariableOrOptional[NotebookTaskParam] = None,
        notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
        pipeline_task: VariableOrOptional[PipelineTaskParam] = None,
        python_wheel_task: VariableOrOptional[PythonWheelTaskParam] = None,
        retry_on_timeout: VariableOrOptional[bool] = None,
        run_if: VariableOrOptional[RunIfParam] = None,
        run_job_task: VariableOrOptional[RunJobTaskParam] = None,
        spark_jar_task: VariableOrOptional[SparkJarTaskParam] = None,
        spark_python_task: VariableOrOptional[SparkPythonTaskParam] = None,
        spark_submit_task: VariableOrOptional[SparkSubmitTaskParam] = None,
        sql_task: VariableOrOptional[SqlTaskParam] = None,
        timeout_seconds: VariableOrOptional[int] = None,
        webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TaskDict(TypedDict, total=False):
    """"""

    task_key: VariableOr[str]
    """
    A unique name for the task. This field is used to refer to this task from other tasks.
    This field is required and must be unique within its parent job.
    On Update or Reset, this field is used to reference the tasks to be updated or reset.
    """

    condition_task: VariableOrOptional[ConditionTaskParam]
    """
    If condition_task, specifies a condition with an outcome that can be used to control the execution of other tasks. Does not require a cluster to execute and does not support retries or notifications.
    """

    dbt_task: VariableOrOptional[DbtTaskParam]
    """
    If dbt_task, indicates that this must execute a dbt task. It requires both Databricks SQL and the ability to use a serverless or a pro SQL warehouse.
    """

    depends_on: VariableOrList[TaskDependencyParam]
    """
    An optional array of objects specifying the dependency graph of the task. All tasks specified in this field must complete before executing this task. The task will run only if the `run_if` condition is true.
    The key is `task_key`, and the value is the name assigned to the dependent task.
    """

    description: VariableOrOptional[str]
    """
    An optional description for this task.
    """

    disable_auto_optimization: VariableOrOptional[bool]
    """
    An option to disable auto optimization in serverless
    """

    email_notifications: VariableOrOptional[TaskEmailNotificationsParam]
    """
    An optional set of email addresses that is notified when runs of this task begin or complete as well as when this task is deleted. The default behavior is to not send any emails.
    """

    environment_key: VariableOrOptional[str]
    """
    The key that references an environment spec in a job. This field is required for Python script, Python wheel and dbt tasks when using serverless compute.
    """

    existing_cluster_id: VariableOrOptional[str]
    """
    If existing_cluster_id, the ID of an existing cluster that is used for all runs.
    When running jobs or tasks on an existing cluster, you may need to manually restart
    the cluster if it stops responding. We suggest running jobs and tasks on new clusters for
    greater reliability
    """

    for_each_task: VariableOrOptional[ForEachTaskParam]
    """
    If for_each_task, indicates that this task must execute the nested task within it.
    """

    health: VariableOrOptional[JobsHealthRulesParam]

    job_cluster_key: VariableOrOptional[str]
    """
    If job_cluster_key, this task is executed reusing the cluster specified in `job.settings.job_clusters`.
    """

    libraries: VariableOrList[LibraryParam]
    """
    An optional list of libraries to be installed on the cluster.
    The default value is an empty list.
    """

    max_retries: VariableOrOptional[int]
    """
    An optional maximum number of times to retry an unsuccessful run. A run is considered to be unsuccessful if it completes with the `FAILED` result_state or `INTERNAL_ERROR` `life_cycle_state`. The value `-1` means to retry indefinitely and the value `0` means to never retry.
    """

    min_retry_interval_millis: VariableOrOptional[int]
    """
    An optional minimal interval in milliseconds between the start of the failed run and the subsequent retry run. The default behavior is that unsuccessful runs are immediately retried.
    """

    new_cluster: VariableOrOptional[ClusterSpecParam]
    """
    If new_cluster, a description of a new cluster that is created for each run.
    """

    notebook_task: VariableOrOptional[NotebookTaskParam]
    """
    If notebook_task, indicates that this task must run a notebook. This field may not be specified in conjunction with spark_jar_task.
    """

    notification_settings: VariableOrOptional[TaskNotificationSettingsParam]
    """
    Optional notification settings that are used when sending notifications to each of the `email_notifications` and `webhook_notifications` for this task.
    """

    pipeline_task: VariableOrOptional[PipelineTaskParam]
    """
    If pipeline_task, indicates that this task must execute a Pipeline.
    """

    python_wheel_task: VariableOrOptional[PythonWheelTaskParam]
    """
    If python_wheel_task, indicates that this job must execute a PythonWheel.
    """

    retry_on_timeout: VariableOrOptional[bool]
    """
    An optional policy to specify whether to retry a job when it times out. The default behavior
    is to not retry on timeout.
    """

    run_if: VariableOrOptional[RunIfParam]
    """
    An optional value specifying the condition determining whether the task is run once its dependencies have been completed.
    
    * `ALL_SUCCESS`: All dependencies have executed and succeeded
    * `AT_LEAST_ONE_SUCCESS`: At least one dependency has succeeded
    * `NONE_FAILED`: None of the dependencies have failed and at least one was executed
    * `ALL_DONE`: All dependencies have been completed
    * `AT_LEAST_ONE_FAILED`: At least one dependency failed
    * `ALL_FAILED`: ALl dependencies have failed
    """

    run_job_task: VariableOrOptional[RunJobTaskParam]
    """
    If run_job_task, indicates that this task must execute another job.
    """

    spark_jar_task: VariableOrOptional[SparkJarTaskParam]
    """
    If spark_jar_task, indicates that this task must run a JAR.
    """

    spark_python_task: VariableOrOptional[SparkPythonTaskParam]
    """
    If spark_python_task, indicates that this task must run a Python file.
    """

    spark_submit_task: VariableOrOptional[SparkSubmitTaskParam]
    """
    If `spark_submit_task`, indicates that this task must be launched by the spark submit script. This task can run only on new clusters.
    
    In the `new_cluster` specification, `libraries` and `spark_conf` are not supported. Instead, use `--jars` and `--py-files` to add Java and Python libraries and `--conf` to set the Spark configurations.
    
    `master`, `deploy-mode`, and `executor-cores` are automatically configured by Databricks; you _cannot_ specify them in parameters.
    
    By default, the Spark submit job uses all available memory (excluding reserved memory for Databricks services). You can set `--driver-memory`, and `--executor-memory` to a smaller value to leave some room for off-heap usage.
    
    The `--jars`, `--py-files`, `--files` arguments support DBFS and S3 paths.
    """

    sql_task: VariableOrOptional[SqlTaskParam]
    """
    If sql_task, indicates that this job must execute a SQL task.
    """

    timeout_seconds: VariableOrOptional[int]
    """
    An optional timeout applied to each run of this job task. A value of `0` means no timeout.
    """

    webhook_notifications: VariableOrOptional[WebhookNotificationsParam]
    """
    A collection of system notification IDs to notify when runs of this task begin or complete. The default behavior is to not send any system notifications.
    """


TaskParam = TaskDict | Task
