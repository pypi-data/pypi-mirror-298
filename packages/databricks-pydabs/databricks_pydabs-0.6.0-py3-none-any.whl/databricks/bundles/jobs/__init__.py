from dataclasses import replace
from datetime import timedelta
from typing import Any, Callable, Optional, ParamSpec, TypeVar, overload

from databricks.bundles.compute.models.environment import Environment, EnvironmentParam
from databricks.bundles.jobs.functions.sql_alert_task import (
    AlertState,
    SqlAlertTaskFunction,
    SqlAlertTaskWithOutput,
)
from databricks.bundles.jobs.functions.sql_file_task import (
    SqlFileTaskFunction,
    SqlFileTaskWithOutput,
)
from databricks.bundles.jobs.functions.sql_query_task import (
    SqlQueryTaskFunction,
    SqlQueryTaskWithOutput,
)
from databricks.bundles.jobs.models.job_environment import (
    JobEnvironment,
    JobEnvironmentParam,
)
from databricks.bundles.jobs.models.job_run_as import JobRunAsParam
from databricks.bundles.jobs.models.jobs_health import (
    JobsHealthRules,
    JobsHealthRulesParam,
)
from databricks.bundles.jobs.models.tasks.dbt_task import DbtTask
from databricks.bundles.jobs.models.tasks.spark_jar_task import SparkJarTask
from databricks.bundles.jobs.models.tasks.spark_python_task import SparkPythonTask
from databricks.bundles.jobs.models.tasks.sql_task_file import SqlTaskFile
from databricks.bundles.jobs.models.trigger import (
    Continuous,
    ContinuousParam,
    TriggerSettings,
    TriggerSettingsParam,
)

__all__ = [
    "AlertState",
    "ClusterSpec",
    "ClusterSpecParam",
    "ComputeTask",
    "ComputeTaskFunction",
    "Continuous",
    "ContinuousParam",
    "CronSchedule",
    "CronScheduleParam",
    "Environment",
    "EnvironmentParam",
    "Job",
    "JobCluster",
    "JobClusterParam",
    "JobEmailNotifications",
    "JobEmailNotificationsParam",
    "JobEnvironment",
    "JobEnvironmentParam",
    "JobFunction",
    "JobNotificationSettings",
    "JobNotificationSettingsParam",
    "JobRunAs",
    "JobRunAsParam",
    "JobSyntaxError",
    "JobsHealthRules",
    "JobsHealthRulesParam",
    "Library",
    "LibraryParam",
    "NotebookTask",
    "Permission",
    "PermissionLevel",
    "PermissionParam",
    "PipelineTask",
    "PythonWheelTask",
    "QueueSettings",
    "QueueSettingsParam",
    "ResourceMutator",
    "SparkJarTask",
    "SparkPythonTask",
    "SqlTask",
    "SqlTaskAlert",
    "SqlTaskDashboard",
    "SqlTaskFile",
    "SqlTaskQuery",
    "SqlTaskSubscription",
    "SqlTaskSubscriptionParam",
    "Task",
    "TaskEmailNotifications",
    "TaskEmailNotificationsParam",
    "TaskFunction",
    "TaskNotificationSettings",
    "TaskNotificationSettingsParam",
    "TaskWithOutput",
    "TriggerSettings",
    "TriggerSettingsParam",
    "WebhookNotifications",
    "WebhookNotificationsParam",
    "dbt_task",
    "jar_task",
    "job",
    "job_mutator",
    "notebook_task",
    "pipeline_task",
    "resource_generator",
    "sql_alert_task",
    "sql_dashboard_task",
    "sql_file_task",
    "sql_notebook_task",
    "sql_query_task",
    "task",
]


from databricks.bundles.compute.models.cluster_spec import ClusterSpec, ClusterSpecParam
from databricks.bundles.compute.models.library import (
    Library,
    LibraryParam,
    PythonPyPiLibrary,
)
from databricks.bundles.internal._transform import (
    _transform_variable_or,
    _transform_variable_or_dict,
    _transform_variable_or_list,
    _transform_variable_or_optional,
)
from databricks.bundles.jobs.functions._signature import Signature
from databricks.bundles.jobs.functions.compute import ComputeTask, ComputeTaskFunction
from databricks.bundles.jobs.functions.job import JobFunction
from databricks.bundles.jobs.functions.task import (
    TaskFunction,
    TaskWithOutput,
    _create_task_with_output,
    _transform_min_retry_interval_millis,
)
from databricks.bundles.jobs.internal.inspections import Inspections
from databricks.bundles.jobs.models.cron_schedule import CronSchedule, CronScheduleParam
from databricks.bundles.jobs.models.email_notifications import (
    JobEmailNotifications,
    JobEmailNotificationsParam,
    JobNotificationSettings,
    JobNotificationSettingsParam,
    TaskEmailNotifications,
    TaskEmailNotificationsParam,
    TaskNotificationSettings,
    TaskNotificationSettingsParam,
)
from databricks.bundles.jobs.models.job import Job
from databricks.bundles.jobs.models.job_cluster import JobCluster, JobClusterParam
from databricks.bundles.jobs.models.job_run_as import JobRunAs
from databricks.bundles.jobs.models.permission import (
    Permission,
    PermissionLevel,
    PermissionParam,
)
from databricks.bundles.jobs.models.queue_settings import (
    QueueSettings,
    QueueSettingsParam,
)
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.models.tasks.notebook_task import NotebookTask
from databricks.bundles.jobs.models.tasks.pipeline_task import PipelineTask
from databricks.bundles.jobs.models.tasks.python_wheel_task import PythonWheelTask
from databricks.bundles.jobs.models.tasks.sql_task import SqlTask
from databricks.bundles.jobs.models.tasks.sql_task_alert import SqlTaskAlert
from databricks.bundles.jobs.models.tasks.sql_task_dashboard import SqlTaskDashboard
from databricks.bundles.jobs.models.tasks.sql_task_query import SqlTaskQuery
from databricks.bundles.jobs.models.tasks.sql_task_subscription import (
    SqlTaskSubscription,
    SqlTaskSubscriptionParam,
)
from databricks.bundles.jobs.models.webhook_notifications import (
    WebhookNotifications,
    WebhookNotificationsParam,
)
from databricks.bundles.resource import ResourceMutator, resource_generator
from databricks.bundles.variables import (
    VariableOr,
    VariableOrDict,
    VariableOrList,
    VariableOrOptional,
    resolve_variable,
)

R = TypeVar("R")
P = ParamSpec("P")

TFunc = TypeVar("TFunc", bound=Callable[..., Any])


@overload
def job(
    *,
    name: VariableOrOptional[str] = None,
    description: VariableOrOptional[str] = None,
    resource_name: Optional[str] = None,
    default_job_cluster_spec: VariableOrOptional[ClusterSpecParam] = None,
    default_environment: VariableOrOptional[EnvironmentParam] = None,
    job_clusters: Optional[VariableOrList[JobClusterParam]] = None,
    max_concurrent_runs: VariableOrOptional[int] = None,
    tags: Optional[VariableOrDict[str]] = None,
    run_as: VariableOrOptional[JobRunAsParam] = None,
    environments: Optional[VariableOrList[JobEnvironmentParam]] = None,
    email_notifications: VariableOrOptional[JobEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[JobNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    schedule: VariableOrOptional[CronScheduleParam] = None,
    trigger: VariableOrOptional[TriggerSettingsParam] = None,
    permissions: Optional[VariableOrList[PermissionParam]] = None,
    queue: VariableOrOptional[QueueSettingsParam] = None,
    continuous: VariableOrOptional[ContinuousParam] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[P, R]], JobFunction[P, R]]:
    """
    A decorator that converts function into :class:`~databricks.bundles.jobs.models.job.Job`.

    Returned function can be called within another job function to trigger a job run, see
    :class:`~databricks.bundles.jobs.functions.job.JobFunction`.

    Example:

    .. code-block:: python

        @task
        def print_hello_world():
            print("Hello World")

        @job(max_concurrent_runs=5)
        def my_job():
            print_hello_world()

    How to use:

    - `Add description or tags to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/tags.html>`_
    - `Add for each task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/for-each.html>`_
    - `Add task dependencies <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/task-dependencies.html>`_
    - `Configure email and system job or task notifications <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/notifications.html>`_
    - `Configure job clusters <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/job-clusters.html>`_
    - `Pass values between tasks <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/pass-task-values.html>`_
    - `Run tasks conditionally <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/conditional-tasks.html>`_
    - `Trigger job runs <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/triggers.html>`_

    :param name: See :attr:`~databricks.bundles.jobs.models.job.Job.name`
    :param description: See :attr:`~databricks.bundles.jobs.models.job.Job.description`
    :param resource_name: See :attr:`~databricks.bundles.resource.Resource.resource_name`
    :param default_job_cluster_spec: Default cluster spec to use for
           :class:`~databricks.bundles.jobs.functions.compute.ComputeTask` in this job.
           See :meth:`~databricks.bundles.jobs.transforms.add_default_job_cluster`.
    :param default_environment:  Default environment ot use for
           :class:`~databricks.bundles.jobs.functions.compute.ComputeTask` in this job.
           See :meth:`~databricks.bundles.jobs.transforms.add_default_job_environment`.
    :param job_clusters: See :attr:`~databricks.bundles.jobs.models.job.Job.job_clusters`
    :param max_concurrent_runs: See :attr:`~databricks.bundles.jobs.models.job.Job.max_concurrent_runs`
    :param tags: See :attr:`~databricks.bundles.jobs.models.job.Job.tags`
    :param run_as: See :attr:`~databricks.bundles.jobs.models.job.Job.run_as`
    :param environments: See :attr:`~databricks.bundles.jobs.models.job.Job.environments`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.job.Job.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.job.Job.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.job.Job.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.job.Job.timeout_seconds`
    :param schedule: See :attr:`~databricks.bundles.jobs.models.job.Job.schedule`
    :param trigger: See :attr:`~databricks.bundles.jobs.models.job.Job.trigger`
    :param permissions: See :attr:`~databricks.bundles.jobs.models.permission.Permission`
    :param queue: See :attr:`~databricks.bundles.jobs.models.job.Job.queue`
    :param continuous: See :attr:`~databricks.bundles.jobs.models.job.Job.continuous`
    :param health: See :attr:`~databricks.bundles.jobs.models.job.Job.health`
    :type: **P** – parameters of annotated function
    :type: **R** – return type of annotated function
    """
    ...


@overload
def job(function: Callable[P, R]) -> JobFunction[P, R]:
    ...


@overload
def task(
    *,
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    libraries: Optional[VariableOrList[LibraryParam]] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
    disable_auto_optimization: VariableOrOptional[bool] = None,
    add_default_library: Optional[bool] = None,
) -> Callable[[Callable[P, R]], ComputeTaskFunction[P, R]]:
    """
    A decorator that converts function into :class:`~databricks.bundles.jobs.functions.python_task.PythonTaskFunction`
    returning :class:`~databricks.bundles.jobs.functions.python_task.PythonTaskWithOutput`.

    Example:

    .. code-block:: python

        @task
        def optimize_table(table: str):
            print(f"Optimizing table {table}")
            spark.sql(f"OPTIMIZE {table}")

    You can pass parameters to a task by adding them to the function signature.

    .. code-block:: python

        @task
        def sum_task(a: int, b: int) -> int:
            return a + b

    See `Pass values between tasks <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/pass-task-values.html>`_.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param libraries: See :attr:`~databricks.bundles.jobs.models.task.Task.libraries`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    :param disable_auto_optimization: See :attr:`~databricks.bundles.jobs.models.task.Task.disable_auto_optimization`
    :param add_default_library: If true or unspecified, adds 'dist/\\*.whl' to 'libraries'
    :type: **P** – parameters of annotated function
    :type: **R** – return type of annotated function
    """
    ...


@overload
def task(function: Callable[P, R]) -> ComputeTaskFunction[P, R]:
    ...


def job(*args: Any, **kwargs: Any) -> Any:
    # using `@job` is equivalent to `@job()`
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return job()(args[0])

    if len(args) != 0:
        raise ValueError("Only keyword args are supported")

    # FIXME needs to be in sync with overload
    def get_wrapper(
        name: VariableOrOptional[str] = None,
        description: VariableOrOptional[str] = None,
        resource_name: Optional[str] = None,
        default_job_cluster_spec: VariableOrOptional[ClusterSpecParam] = None,
        default_environment: VariableOrOptional[EnvironmentParam] = None,
        job_clusters: Optional[VariableOrList[JobClusterParam]] = None,
        max_concurrent_runs: VariableOrOptional[int] = None,
        tags: Optional[VariableOrDict[str]] = None,
        run_as: VariableOrOptional[JobRunAsParam] = None,
        email_notifications: VariableOrOptional[JobEmailNotificationsParam] = None,
        webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
        notification_settings: VariableOrOptional[JobNotificationSettingsParam] = None,
        timeout_seconds: VariableOrOptional[int] = None,
        schedule: VariableOrOptional[CronScheduleParam] = None,
        trigger: VariableOrOptional[TriggerSettingsParam] = None,
        environments: Optional[VariableOrList[JobEnvironmentParam]] = None,
        permissions: Optional[VariableOrList[PermissionParam]] = None,
        queue: VariableOrOptional[QueueSettingsParam] = None,
        health: VariableOrOptional[JobsHealthRulesParam] = None,
    ) -> Callable[[Callable[P, R]], JobFunction[P, R]]:
        if default_job_cluster_spec:
            default_job_cluster = JobCluster(
                job_cluster_key=JobCluster.DEFAULT_KEY,
                new_cluster=_transform_variable_or(
                    ClusterSpec, default_job_cluster_spec
                ),
            )
        else:
            default_job_cluster = None

        if default_environment:
            default_job_environment = JobEnvironment(
                environment_key=JobCluster.DEFAULT_KEY,
                spec=_transform_variable_or(Environment, default_environment),
            )
        else:
            default_job_environment = None

        base_job = Job(
            job_clusters=_transform_variable_or_list(JobCluster, job_clusters or []),
            max_concurrent_runs=max_concurrent_runs,
            schedule=_transform_variable_or_optional(CronSchedule, schedule),
            trigger=_transform_variable_or_optional(TriggerSettings, trigger),
            tags=_transform_variable_or_dict(str, tags or {}),
            run_as=_transform_variable_or_optional(JobRunAs, run_as),
            environments=_transform_variable_or_list(
                JobEnvironment, environments or []
            ),
            email_notifications=_transform_variable_or_optional(
                JobEmailNotifications, email_notifications
            ),
            webhook_notifications=_transform_variable_or_optional(
                WebhookNotifications, webhook_notifications
            ),
            notification_settings=_transform_variable_or_optional(
                JobNotificationSettings, notification_settings
            ),
            timeout_seconds=timeout_seconds,
            permissions=_transform_variable_or_list(Permission, permissions or []),
            queue=_transform_variable_or_optional(QueueSettings, queue),
            health=_transform_variable_or_optional(JobsHealthRules, health),
            name=name,
            description=description,
            resource_name=resource_name,
        )

        def wrapper(function: Callable[P, R]) -> JobFunction[P, R]:
            return JobFunction.from_job_function(
                function,
                default_job_cluster=default_job_cluster,
                default_job_environment=default_job_environment,
                base_job=base_job,
            )

        return wrapper

    return get_wrapper(**kwargs)


def task(*args: Any, **kwargs: Any) -> Any:
    # using `@task` is equivalent to `@task()`
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        return task()(args[0])

    def get_wrapper(
        max_retries: VariableOrOptional[int] = None,
        min_retry_interval_millis: VariableOrOptional[timedelta] = None,
        retry_on_timeout: VariableOrOptional[bool] = None,
        email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
        webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
        notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
        timeout_seconds: VariableOrOptional[int] = None,
        libraries: Optional[VariableOrList[LibraryParam]] = None,
        add_default_library: Optional[bool] = None,
        health: VariableOrOptional[JobsHealthRulesParam] = None,
        disable_auto_optimization: VariableOrOptional[bool] = None,
    ) -> Callable[[Callable[P, R]], ComputeTaskFunction[P, R]]:
        def wrapper(function: Callable[P, R]) -> ComputeTaskFunction[P, R]:
            task_func_name = Inspections.get_task_func_name(function)
            task_key = Inspections.get_simple_name(function)
            base_task = _create_compute_task(
                task_key=task_key,
                max_retries=max_retries,
                min_retry_interval_millis=min_retry_interval_millis,
                retry_on_timeout=retry_on_timeout,
                email_notifications=email_notifications,
                webhook_notifications=webhook_notifications,
                notification_settings=notification_settings,
                timeout_seconds=timeout_seconds,
                libraries=libraries,
                health=health,
                disable_auto_optimization=disable_auto_optimization,
            )

            if add_default_library or add_default_library is None:
                updated_libraries = [
                    *resolve_variable(base_task.libraries),
                    Library.create(whl="dist/*.whl"),
                ]
            else:
                updated_libraries = base_task.libraries

            base_task = replace(
                base_task,
                python_wheel_task=PythonWheelTask(
                    package_name="databricks-pydabs",
                    entry_point="entrypoint",
                    parameters=[f"--task_func={task_func_name}"],
                ),
                libraries=updated_libraries,
            )

            return ComputeTaskFunction(
                function=function,
                base_task=base_task,
            )

        return wrapper

    return get_wrapper(**kwargs)


def notebook_task(
    *,
    notebook_path: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    libraries: Optional[VariableOrList[LibraryParam]] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
    disable_auto_optimization: VariableOrOptional[bool] = None,
) -> Callable[[Callable[P, None]], ComputeTaskFunction[P, None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.compute.ComputeTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.notebook_task.NotebookTask`.

    You can pass parameters to a notebook by adding them to the function signature.

    You can return values from a notebook using
    :class:`~databricks.bundles.jobs.functions.compute.ComputeTask.TaskValues`.

    Example:

    .. code-block:: python

        @notebook_task(notebook_path="notebooks/my_notebook.ipynb")
        def my_notebook(my_param: str):
            pass

    See `Add a notebook task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/notebook-task.html#python-notebook-task>`_

    :param notebook_path: Local path to a notebook relative to the bundle root.
        or absolute path to a notebook in the Databricks workspace.
        See :attr:`~databricks.bundles.jobs.models.tasks.notebook_task.NotebookTask.notebook_path`

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param libraries: See :attr:`~databricks.bundles.jobs.models.task.Task.libraries`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    :param disable_auto_optimization: See :attr:`~databricks.bundles.jobs.models.task.Task.disable_auto_optimization`
    :type: **P** – parameters of annotated function
    """

    def wrapper(function: Callable[P, None]) -> ComputeTaskFunction[P, None]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_compute_task(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            libraries=libraries,
            health=health,
            disable_auto_optimization=disable_auto_optimization,
        )

        base_task = replace(
            base_task,
            notebook_task=NotebookTask(
                notebook_path=notebook_path,
            ),
        )

        return ComputeTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def sql_notebook_task(
    *,
    notebook_path: VariableOr[str],
    warehouse_id: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[P, None]], TaskFunction[P, None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.task.TaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.notebook_task.NotebookTask`, requires a SQL warehouse.

    You can pass parameters to a notebook by adding them to the function signature.

    Example:

    .. code-block:: python

        @notebook_task(notebook_path="notebooks/my_notebook.ipynb")
        def my_notebook(my_param: str):
            pass

    See `Add a notebook task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/notebook-task.html#python-notebook-task>`_

    :param notebook_path: Local path to a notebook relative to the bundle root.
        or absolute path to a notebook in the Databricks workspace.
        See :attr:`~databricks.bundles.jobs.models.tasks.notebook_task.NotebookTask.notebook_path`

    :param warehouse_id: SQL warehouse to run the notebook.
        Only serverless and pro SQL warehouses are supported, classic SQL warehouses are not supported.
        Note that SQL warehouses only support SQL cells; if the notebook contains non-SQL cells, the run will fail.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[P, None]) -> TaskFunction[P, None]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
        )

        base_task = replace(
            base_task,
            notebook_task=NotebookTask(
                notebook_path=notebook_path,
                warehouse_id=warehouse_id,
            ),
        )

        return TaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def jar_task(
    *,
    main_class_name: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    libraries: Optional[VariableOrList[LibraryParam]] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
    disable_auto_optimization: VariableOrOptional[bool] = None,
) -> Callable[[Callable[P, None]], ComputeTaskFunction[P, None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.compute.ComputeTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.spark_jar_task.SparkJarTask`.

    :param main_class_name: See :attr:`~databricks.bundles.jobs.models.tasks.spark_jar_task.SparkJarTask.main_class_name`
    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param libraries: See :attr:`~databricks.bundles.jobs.models.task.Task.libraries`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    :param disable_auto_optimization: See :attr:`~databricks.bundles.jobs.models.task.Task.disable_auto_optimization`
    """

    def wrapper(function: Callable[P, None]) -> ComputeTaskFunction[P, None]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_compute_task(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            libraries=libraries,
            health=health,
            disable_auto_optimization=disable_auto_optimization,
        )

        base_task = replace(
            base_task,
            spark_jar_task=SparkJarTask(
                main_class_name=main_class_name,
            ),
        )

        return ComputeTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def python_file_task(
    *,
    python_file: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    libraries: Optional[VariableOrList[LibraryParam]] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
    disable_auto_optimization: VariableOrOptional[bool] = None,
) -> Callable[[Callable[P, None]], ComputeTaskFunction[P, None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.compute.ComputeTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.spark_python_task.SparkPythonTask`.

    :param python_file: See :attr:`~databricks.bundles.jobs.models.tasks.spark_python_task.SparkPythonTask.python_file`
    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param libraries: See :attr:`~databricks.bundles.jobs.models.task.Task.libraries`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    :param disable_auto_optimization: See :attr:`~databricks.bundles.jobs.models.task.Task.disable_auto_optimization`
    """

    def wrapper(function: Callable[P, None]) -> ComputeTaskFunction[P, None]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_compute_task(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            libraries=libraries,
            health=health,
            disable_auto_optimization=disable_auto_optimization,
        )

        base_task = replace(
            base_task,
            spark_python_task=SparkPythonTask(
                python_file=python_file,
            ),
        )

        return ComputeTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def pipeline_task(
    *,
    pipeline_id: VariableOr[str],
    full_refresh: VariableOrOptional[bool] = None,
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[[], None]], TaskFunction[[], None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.task.TaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.pipeline_task.PipelineTask`.

    Adding parameters to decorated function is not supported, and there is no output.

    Example:

    .. code-block:: python

        @pipeline_task(
            pipeline_id="${resources.pipelines.my_pipeline.id}",
            full_refresh=False,
        )
        def run_pipeline_task():
            pass

    See `Add a pipeline task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/pipeline-task.html>`_

    :param pipeline_id:
        ID of the target Delta Live Tables pipeline.

        See :attr:`~databricks.bundles.jobs.models.tasks.pipeline_task.PipelineTask.pipeline_id`

    :param full_refresh:
        If true, triggers a full refresh on the delta live table.

        See :attr:`~databricks.bundles.jobs.models.tasks.pipeline_task.PipelineTask.full_refresh`

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[[], None]) -> TaskFunction[[], None]:
        signature = Signature.from_function(function)

        if signature.parameters:
            raise ValueError("Parameters are not supported for pipeline task")

        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
        )

        base_task = replace(
            base_task,
            pipeline_task=PipelineTask(
                pipeline_id=pipeline_id,
                full_refresh=full_refresh,
            ),
        )

        return TaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def dbt_task(
    *,
    commands: VariableOrList[str],
    project_directory: VariableOr[str],
    schema: VariableOrOptional[str] = None,
    warehouse_id: VariableOrOptional[str] = None,
    profiles_directory: VariableOrOptional[str] = None,
    catalog: VariableOrOptional[str] = None,
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    libraries: Optional[VariableOrList[LibraryParam]] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
    disable_auto_optimization: VariableOrOptional[bool] = None,
) -> Callable[[Callable[[], None]], ComputeTaskFunction[[], None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.compute.ComputeTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask`.

    Adding parameters to decorated function is not supported, and there is no output.

    Example:

    .. code-block:: python

        @dbt_task(
            commands=[
                "dbt deps --target=${bundle.target}",
                "dbt seed --target=${bundle.target}",
                "dbt run --target=${bundle.target}",
            ],
            project_directory="dbt_project",
            profiles_directory="dbt_profiles",
        )
        def my_dbt_task():
            pass

    :param commands:
        List of dbt commands to run.
        See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.commands`

    :param project_directory: See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.profiles_directory`
    :param schema: See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.schema`
    :param warehouse_id: See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.warehouse_id`
    :param profiles_directory: See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.profiles_directory`
    :param catalog: See :attr:`~databricks.bundles.jobs.models.tasks.dbt_task.DbtTask.catalog`

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param libraries: See :attr:`~databricks.bundles.jobs.models.task.Task.libraries`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    :param disable_auto_optimization: See :attr:`~databricks.bundles.jobs.models.task.Task.disable_auto_optimization`
    """

    if libraries is None:
        libraries = [
            Library(pypi=PythonPyPiLibrary(package="dbt-databricks>=1.0.0,<2.0.0"))
        ]

    def wrapper(function: Callable[P, None]) -> ComputeTaskFunction[P, None]:
        signature = Signature.from_function(function)
        task_key = Inspections.get_simple_name(function)

        if signature.parameters:
            raise ValueError("Parameters are not supported for dbt task")

        base_task = _create_compute_task(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            libraries=libraries,
            health=health,
            disable_auto_optimization=disable_auto_optimization,
        )

        base_task = replace(
            base_task,
            dbt_task=DbtTask(
                commands=_transform_variable_or_list(str, commands),
                project_directory=project_directory,
                schema=schema,
                warehouse_id=warehouse_id,
                profiles_directory=profiles_directory,
                catalog=catalog,
            ),
        )

        return ComputeTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def sql_dashboard_task(
    *,
    warehouse_id: VariableOr[str],
    dashboard_id: VariableOr[str],
    subscriptions: Optional[VariableOrList[SqlTaskSubscriptionParam]] = None,
    pause_subscriptions: VariableOrOptional[bool] = None,
    custom_subject: VariableOrOptional[str] = None,
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[P, None]], TaskFunction[P, None]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.task.TaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask` and
    :class:`~databricks.bundles.jobs.models.tasks.sql_task_dashboard.SqlTaskDashboard`.

    You can pass parameters to the dashboard by adding them to the function signature.

    See `Add a SQL dashboard task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/sql-query-dashboard.html>`_

    :param warehouse_id:
        ID of the SQL warehouse. Only serverless or pro SQL warehouses are supported.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask.warehouse_id`.

    :param dashboard_id:
        ID of the SQL dashboard.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_dashboard.SqlTaskDashboard.dashboard_id`.

    :param pause_subscriptions:
        If true, pauses all subscriptions for the dashboard.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_dashboard.SqlTaskDashboard.pause_subscriptions`.

    :param subscriptions:
        If specified, dashboard snapshots are sent to subscriptions.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_dashboard.SqlTaskDashboard.subscriptions`.

    :param custom_subject:
        Subject of the email sent to subscribers of this task.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_dashboard.SqlTaskDashboard.custom_subject`.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[P, None]) -> TaskFunction[P, None]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
        )

        base_task = replace(
            base_task,
            sql_task=SqlTask(
                warehouse_id=warehouse_id,
                dashboard=SqlTaskDashboard(
                    dashboard_id=dashboard_id,
                    subscriptions=_transform_variable_or_list(
                        SqlTaskSubscription, subscriptions or []
                    ),
                    custom_subject=custom_subject,
                    pause_subscriptions=pause_subscriptions,
                ),
            ),
        )

        return TaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def sql_query_task(
    *,
    warehouse_id: VariableOr[str],
    query_id: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[P, Optional[list[R]]]], SqlQueryTaskFunction[P, R]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.sql_query_task.SqlQueryTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask` and
    :class:`~databricks.bundles.jobs.models.tasks.sql_task_query.SqlTaskQuery`.

    You can pass parameters to the query by adding them to the function signature.

    See `Add a SQL query task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/sql-query-task.html>`_

    :param warehouse_id:
        ID of the SQL warehouse. Only serverless or pro SQL warehouses are supported.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask.warehouse_id`.

    :param query_id:
        ID of the SQL query. See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_query.SqlTaskQuery.query_id`.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[P, Optional[list[R]]]) -> SqlQueryTaskFunction[P, R]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
            cls=SqlQueryTaskWithOutput,
        )

        base_task = replace(
            base_task,
            sql_task=SqlTask(
                warehouse_id=warehouse_id,
                query=SqlTaskQuery(
                    query_id=query_id,
                ),
            ),
        )

        return SqlQueryTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def sql_alert_task(
    *,
    warehouse_id: VariableOr[str],
    alert_id: VariableOr[str],
    subscriptions: VariableOrList[SqlTaskSubscriptionParam],
    pause_subscriptions: VariableOrOptional[bool] = None,
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[[], None]], SqlAlertTaskFunction]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.sql_alert_task.SqlAlertTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask` and
    :class:`~databricks.bundles.jobs.models.tasks.sql_task_alert.SqlTaskAlert` and returning task with
    :class:`~databricks.bundles.jobs.functions.sql_alert_task.SqlAlertTaskOutput`.

    Decorated function can't have any parameters.

    See `Add a SQL alert task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/sql-alert-task.html>`_

    :param warehouse_id:
        ID of the SQL warehouse. Only serverless or pro SQL warehouses are supported.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask.warehouse_id`.

    :param alert_id:
        ID of the SQL alert.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_alert.SqlTaskAlert.alert_id`.

    :param subscriptions:
        List of subscriptions to send alert notifications.

        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_alert.SqlTaskAlert.subscriptions`.

    :param pause_subscriptions:
        If true, the alert notifications are not sent to subscriptions.

        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_alert.SqlTaskAlert.pause_subscriptions`.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[P, None]) -> SqlAlertTaskFunction:
        signature = Signature.from_function(function)

        if signature.parameters:
            raise ValueError("Parameters are not supported for SQL alert task")

        if not subscriptions:
            raise ValueError(
                "At least one subscription for SQL alert task must be specified"
            )

        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
            cls=SqlAlertTaskWithOutput,
        )

        base_task = replace(
            base_task,
            sql_task=SqlTask(
                warehouse_id=warehouse_id,
                alert=SqlTaskAlert(
                    alert_id=alert_id,
                    subscriptions=_transform_variable_or_list(
                        SqlTaskSubscription, subscriptions
                    ),
                    pause_subscriptions=pause_subscriptions,
                ),
            ),
        )

        return SqlAlertTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


def sql_file_task(
    *,
    warehouse_id: VariableOr[str],
    path: VariableOr[str],
    max_retries: VariableOrOptional[int] = None,
    min_retry_interval_millis: VariableOrOptional[timedelta] = None,
    retry_on_timeout: VariableOrOptional[bool] = None,
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam] = None,
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam] = None,
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam] = None,
    timeout_seconds: VariableOrOptional[int] = None,
    health: VariableOrOptional[JobsHealthRulesParam] = None,
) -> Callable[[Callable[P, Optional[list[R]]]], SqlFileTaskFunction[P, R]]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.jobs.functions.sql_file_task.SqlFileTaskFunction`
    containing :class:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask` and
    :class:`~databricks.bundles.jobs.models.tasks.sql_task_file.SqlTaskFile`.

    You can pass parameters to SQL statements by adding them to the function signature.

    See `Add a SQL file task to a job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/sql-file-task.html>`_

    :param warehouse_id:
        ID of the SQL warehouse. Only serverless or pro SQL warehouses are supported.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task.SqlTask.warehouse_id`.
    :param path:
        Path to a SQL file relative to the bundle root.
        See :attr:`~databricks.bundles.jobs.models.tasks.sql_task_file.SqlTaskFile.path`.

    :param max_retries: See :attr:`~databricks.bundles.jobs.models.task.Task.max_retries`
    :param min_retry_interval_millis: See :attr:`~databricks.bundles.jobs.models.task.Task.min_retry_interval_millis`
    :param retry_on_timeout: See :attr:`~databricks.bundles.jobs.models.task.Task.retry_on_timeout`
    :param email_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.email_notifications`
    :param webhook_notifications: See :attr:`~databricks.bundles.jobs.models.task.Task.webhook_notifications`
    :param notification_settings: See :attr:`~databricks.bundles.jobs.models.task.Task.notification_settings`
    :param timeout_seconds: See :attr:`~databricks.bundles.jobs.models.task.Task.timeout_seconds`
    :param health: See :attr:`~databricks.bundles.jobs.models.task.Task.health`
    """

    def wrapper(function: Callable[P, Optional[list[R]]]) -> SqlFileTaskFunction[P, R]:
        task_key = Inspections.get_simple_name(function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=max_retries,
            min_retry_interval_millis=min_retry_interval_millis,
            retry_on_timeout=retry_on_timeout,
            email_notifications=email_notifications,
            webhook_notifications=webhook_notifications,
            notification_settings=notification_settings,
            timeout_seconds=timeout_seconds,
            health=health,
            cls=SqlFileTaskWithOutput,
        )

        base_task = replace(
            base_task,
            sql_task=SqlTask(
                warehouse_id=warehouse_id,
                file=SqlTaskFile(
                    path=path,
                ),
            ),
        )

        return SqlFileTaskFunction(
            function=function,
            base_task=base_task,
        )

    return wrapper


class JobSyntaxError(SyntaxError):
    pass


def _create_compute_task(
    task_key: VariableOr[str],
    max_retries: VariableOrOptional[int],
    min_retry_interval_millis: VariableOrOptional[timedelta],
    retry_on_timeout: VariableOrOptional[bool],
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam],
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam],
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam],
    timeout_seconds: VariableOrOptional[int],
    libraries: Optional[VariableOrList[LibraryParam]],
    health: VariableOrOptional[JobsHealthRulesParam],
    disable_auto_optimization: VariableOrOptional[bool],
) -> ComputeTask:
    return ComputeTask(
        task_key=task_key,
        max_retries=max_retries,
        min_retry_interval_millis=_transform_min_retry_interval_millis(
            min_retry_interval_millis
        ),
        retry_on_timeout=retry_on_timeout,
        email_notifications=_transform_variable_or_optional(
            TaskEmailNotifications, email_notifications
        ),
        webhook_notifications=_transform_variable_or_optional(
            WebhookNotifications, webhook_notifications
        ),
        notification_settings=_transform_variable_or_optional(
            TaskNotificationSettings, notification_settings
        ),
        timeout_seconds=timeout_seconds,
        libraries=_transform_variable_or_list(Library, libraries or []),
        health=_transform_variable_or_optional(JobsHealthRules, health),
        disable_auto_optimization=disable_auto_optimization,
    )


def job_mutator(function: Callable[[Job], Job]) -> ResourceMutator[Job]:
    """
    A decorator that converts a function into :class:`~databricks.bundles.resource.ResourceMutator`,
    allowing to modifying jobs defined in the bundle before they are deployed.

    Job mutators are applied for each job defined in the bundle, including jobs defined in YAML.
    Jobs are updated with returned value of the decorated function.

    Example:

    .. code-block:: python

        from dataclasses import replace
        from databricks.bundles.jobs import Job, job_mutator

        @job_mutator
        def add_tag_to_job(job: Job) -> Job:
            \"""
            Automatically set "owner" on each job that doesn't specify it.
            \"""

            new_tags = job.tags
            if "owner" not in job.tags:
                new_tags = {"owner": "default", **new_tags}

            return replace(job, tags=new_tags)

    See `Apply settings to every job <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/job-mutators.html>`_

    Note: Mutators defined within a single Python module are applied in the order they are defined.
    The relative order of mutators defined in different modules is not guaranteed.
    """

    return ResourceMutator(resource_type=Job, function=function)


def _resolve_recursive_imports():
    import typing

    from databricks.bundles.jobs.models.tasks.for_each_task import ForEachTask

    ForEachTask.__annotations__ = typing.get_type_hints(
        ForEachTask,
        globalns={"Task": Task, "VariableOr": VariableOr},
    )


_resolve_recursive_imports()
