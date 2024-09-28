import dataclasses
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, ParamSpec, TypeVar

from databricks.bundles.compute.models.library import Library, LibraryParam
from databricks.bundles.internal._transform import _transform_variable_or_list
from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput
from databricks.bundles.variables import VariableOr, VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "ComputeTask",
    "ComputeTaskFunction",
]

R = TypeVar("R")
P = ParamSpec("P")


@dataclass(kw_only=True)
class ComputeTask(Generic[R], TaskWithOutput):
    """
    Compute tasks are tasks running on existing clusters, job clusters, or serverless
    compute.
    """

    class TaskValues:
        """
        Task values are used to share information between tasks.

        In this example, `first_task` sets value for key `my_value` and `second_task` reads it.

        .. code-block:: python

            @task
            def first_task():
                dbutils.jobs.taskValues.set("my_value", 42)

            @task
            def second_task(value: int):
                print(value)

            def my_job():
                first = first_task()

                second_task(first.values.my_value)

        See `Share information between tasks in a Databricks job
        <https://docs.databricks.com/en/jobs/share-task-context.html>`_
        """

        def __getattribute__(self, item) -> Any:
            pass

    def with_existing_cluster_id(self, value: VariableOr[str]) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.existing_cluster_id` with a new value,
        :attr:`~databricks.bundles.jobs.models.task.Task.job_cluster_key`,
        :attr:`~databricks.bundles.jobs.models.task.Task.new_cluster` and
        :attr:`~databricks.bundles.jobs.models.task.Task.environment_key` are set to none.
        """

        return dataclasses.replace(
            self,
            existing_cluster_id=value,
            job_cluster_key=None,
            environment_key=None,
            new_cluster=None,
        )

    def with_job_cluster_key(self, value: str) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.job_cluster_key` with a new value,
        :attr:`~databricks.bundles.jobs.models.task.Task.existing_cluster_id`,
        :attr:`~databricks.bundles.jobs.models.task.Task.new_cluster` and
        :attr:`~databricks.bundles.jobs.models.task.Task.environment_key` are set to none.
        """

        return dataclasses.replace(
            self,
            job_cluster_key=value,
            existing_cluster_id=None,
            environment_key=None,
            new_cluster=None,
        )

    def with_environment_key(self, value: str) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.environment_key` with a new value,
        :attr:`~databricks.bundles.jobs.models.task.Task.existing_cluster_id`,
        :attr:`~databricks.bundles.jobs.models.task.Task.new_cluster` and
        :attr:`~databricks.bundles.jobs.models.task.Task.job_cluster_key` are set to none.

        Note: tasks using :attr:`~databricks.bundles.jobs.models.task.Task.environment_key` can't use
        :attr:`~databricks.bundles.jobs.models.task.Task.libraries`, and need to clear them using
        :meth:`~databricks.bundles.jobs.functions.compute.ComputeTask.with_libraries`.
        """

        return dataclasses.replace(
            self,
            environment_key=value,
            existing_cluster_id=None,
            job_cluster_key=None,
            new_cluster=None,
        )

    def with_libraries(self, libraries: VariableOrList[LibraryParam]) -> "Self":
        """
        Override :attr:`~databricks.bundles.jobs.models.task.Task.libraries` with new cluster libraries.
        """

        return dataclasses.replace(
            self, libraries=_transform_variable_or_list(Library, libraries)
        )

    @property
    def values(self) -> TaskValues:
        """
        Access values set by this task. See :class:`TaskValues` for more information.
        """

        raise Exception(
            "Accessing task values outside of @job decorator isn't supported"
        )

    @property
    def result(self) -> R:
        """
        Returns task result. For functions decorated with
        :func:`@task <databricks.bundles.jobs.task>`, it's their return value.
        """

        raise Exception(
            "Accessing task result outside of @job decorator isn't supported"
        )


@dataclass(kw_only=True, frozen=True)
class ComputeTaskFunction(TaskFunction[P, R]):
    """
    Returns :class:`ComputeTask` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.
    """

    base_task: ComputeTask[R]

    def __call__(self, /, *args: P.args, **kwargs: P.kwargs) -> ComputeTask[R]:
        return super().__call__(*args, **kwargs)  # type:ignore
