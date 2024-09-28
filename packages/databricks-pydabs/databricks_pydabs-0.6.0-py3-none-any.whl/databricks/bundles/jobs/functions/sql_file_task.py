from dataclasses import dataclass
from typing import Generic, Optional, ParamSpec, TypeVar

from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(kw_only=True)
class SqlFileTaskOutput(Generic[R]):
    rows: list[R]
    first_row: R


@dataclass
class SqlFileTaskWithOutput(Generic[R], TaskWithOutput):
    """
    SQL file task with output properties.

    See also :meth:`~databricks.bundles.jobs.sql_file_task`.
    """

    @property
    def output(self) -> SqlFileTaskOutput[R]:
        raise Exception(
            "Accessing task output outside of @job decorator isn't supported"
        )

    @property
    def result(self) -> list[R]:
        """
        Alias for `.output.rows`
        """

        raise Exception(
            "Accessing task output outside of @job decorator isn't supported"
        )


class SqlFileTaskFunction(TaskFunction[P, Optional[list[R]]]):
    """
    Returns :class:`SqlFileTaskWithOutput` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.

    See also :meth:`~databricks.bundles.jobs.sql_file_task`.
    """

    base_task: SqlFileTaskWithOutput[R]

    def __call__(
        self, /, *args: P.args, **kwargs: P.kwargs
    ) -> SqlFileTaskWithOutput[R]:
        return super().__call__(*args, **kwargs)  # type:ignore
