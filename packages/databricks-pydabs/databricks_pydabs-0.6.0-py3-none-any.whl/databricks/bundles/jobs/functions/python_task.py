from typing import ParamSpec, TypeVar

from databricks.bundles.jobs.functions.compute import ComputeTask, ComputeTaskFunction

__all__ = [
    "PythonTaskFunction",
    "PythonTaskWithOutput",
]

R = TypeVar("R")
P = ParamSpec("P")


class PythonTaskWithOutput(ComputeTask[R]):
    @property
    def result(self) -> R:
        """
        Returns task result containing the return value of the decorated function.
        """

        raise Exception(
            "Accessing task result outside of @job decorator isn't supported"
        )


class PythonTaskFunction(ComputeTaskFunction[P, R]):
    """
    Returns :class:`PythonTaskWithOutput` when called within function annotated with
    :func:`@task <databricks.bundles.jobs.task>`.
    """

    base_task: PythonTaskWithOutput[R]

    def __call__(self, /, *args: P.args, **kwargs: P.kwargs) -> PythonTaskWithOutput[R]:
        return super().__call__(*args, **kwargs)  # type:ignore
