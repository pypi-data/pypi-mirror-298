from dataclasses import dataclass
from typing import Generic, Optional, ParamSpec, TypeVar

from databricks.bundles.jobs.functions.task import TaskFunction, TaskWithOutput

P = ParamSpec("P")
R = TypeVar("R")


@dataclass(kw_only=True)
class SqlQueryTaskOutput(Generic[R]):
    rows: list[R]
    first_row: R


class SqlQueryTaskWithOutput(Generic[R], TaskWithOutput):
    """
    SQL query task with output properties.

    See also :meth:`~databricks.bundles.jobs.sql_query_task`.
    """

    @property
    def output(self) -> SqlQueryTaskOutput[R]:
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


class SqlQueryTaskFunction(TaskFunction[P, Optional[list[R]]]):
    """
    Returns :class:`SqlQueryTaskWithOutput` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.

    See also :meth:`~databricks.bundles.jobs.sql_query_task`.
    """

    base_task: SqlQueryTaskWithOutput[R]

    def __call__(
        self, /, *args: P.args, **kwargs: P.kwargs
    ) -> SqlQueryTaskWithOutput[R]:
        return super().__call__(*args, **kwargs)  # type:ignore
