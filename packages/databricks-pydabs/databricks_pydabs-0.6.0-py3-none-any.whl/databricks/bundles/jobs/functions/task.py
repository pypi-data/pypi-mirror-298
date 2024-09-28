import copy
from dataclasses import dataclass, replace
from datetime import timedelta
from typing import TYPE_CHECKING, Callable, Generic, ParamSpec, Type, TypeVar

from databricks.bundles.internal._transform import (
    _transform_variable_or_optional,
)
from databricks.bundles.jobs.functions._task_parameters import _TaskParameters
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
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.models.task_dependency import TaskDependency
from databricks.bundles.jobs.models.webhook_notifications import (
    WebhookNotifications,
    WebhookNotificationsParam,
)
from databricks.bundles.variables import (
    Variable,
    VariableOr,
    VariableOrOptional,
    resolve_variable,
)

if TYPE_CHECKING:
    from typing_extensions import Self


R = TypeVar("R")
P = ParamSpec("P")


@dataclass(kw_only=True)
class TaskWithOutput(Task):
    """
    Extends :class:`~databricks.bundles.jobs.models.task.Task` with additional
    methods for applicable within functions annotated with :class:`@job <databricks.bundles.jobs.job>`.
    """

    def with_task_key(self, value: str) -> "Self":
        """
        Unique identifier for the task. Most of the decorators automatically set this value
        using the function name. If task is assigned to a variable within function annotated with
        @job decorator, it's using the variable name as a task key.

        See :attr:`~databricks.bundles.jobs.models.task.Task.task_key`.
        """

        return replace(self, task_key=value)

    def add_depends_on(self, task: Task) -> "Self":
        """
        Adds a dependency on the specified task. See :attr:`~databricks.bundles.jobs.models.task.Task.depends_on`.

        Note: if a task output is as a task parameter, it's added as a dependency automatically.
        """

        if not task.task_key:
            raise ValueError("Specified task doesn't have task_key")

        task_dependency = TaskDependency(task.task_key)
        depends_on = resolve_variable(self.depends_on)

        # FIXME test it
        if task_dependency in depends_on:
            return self

        return replace(self, depends_on=[*depends_on, task_dependency])

    def with_run_if(self, run_if: VariableOrOptional[RunIfParam]) -> "Self":
        """
        Set the condition determining whether the task is run once its dependencies have been completed.

        See :attr:`~databricks.bundles.jobs.models.task.Task.run_if`.
        """

        return replace(self, run_if=_transform_variable_or_optional(RunIf, run_if))


@dataclass(kw_only=True, frozen=True)
class TaskFunction(Generic[P, R]):
    function: Callable[P, R]
    """
    Underling function that was decorated. Can be accessed for unit-testing.
    
    Example:
    
    .. code-block:: python
    
        # in src/my_bundle/hello_world.py
        from databricks.bundles import task
        
        @task
        def sum_task(a: int, b: int) -> int:
            return a + b
            
        # in tests/test_hello_world.py
        from my_bundle.hello_world import sum_task
        
        def test_hello_world():
            assert sum.task.function(1, 2) == 3
        
    
    See `Testing job tasks <https://docs.databricks.com/en/dev-tools/bundles/python/testing.html>`_.
    """

    base_task: TaskWithOutput
    """
    :meta private: reserved for internal use
    """

    def __call__(self, /, *args: P.args, **kwargs: P.kwargs) -> TaskWithOutput:
        task_parameters = _TaskParameters.parse_call(self.function, args, kwargs)
        # deep copy to avoid mutating shared instance
        base_task_copy = copy.deepcopy(self.base_task)
        base_task_with_parameters = task_parameters.inject(base_task_copy)

        return base_task_with_parameters


def _transform_min_retry_interval_millis(
    min_retry_interval_millis: VariableOrOptional[timedelta],
) -> VariableOrOptional[int]:
    if not min_retry_interval_millis:
        return None

    if isinstance(min_retry_interval_millis, Variable):
        # FIXME specified variable should be an int with milliseconds, not timedelta
        # we should allow to specify timedelta as well
        return Variable(path=min_retry_interval_millis.path, type=int)

    if min_retry_interval_millis.microseconds:
        raise ValueError("Microseconds are not supported for 'min_retry_interval'")

    return min_retry_interval_millis // timedelta(milliseconds=1)


_TaskT = TypeVar("_TaskT", bound=TaskWithOutput)


def _create_task_with_output(
    task_key: VariableOr[str],
    max_retries: VariableOrOptional[int],
    min_retry_interval_millis: VariableOrOptional[timedelta],
    retry_on_timeout: VariableOrOptional[bool],
    email_notifications: VariableOrOptional[TaskEmailNotificationsParam],
    webhook_notifications: VariableOrOptional[WebhookNotificationsParam],
    notification_settings: VariableOrOptional[TaskNotificationSettingsParam],
    timeout_seconds: VariableOrOptional[int],
    health: VariableOrOptional[JobsHealthRulesParam],
    cls: Type[_TaskT] = TaskWithOutput,
) -> _TaskT:
    return cls(
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
        health=_transform_variable_or_optional(JobsHealthRules, health),
    )
