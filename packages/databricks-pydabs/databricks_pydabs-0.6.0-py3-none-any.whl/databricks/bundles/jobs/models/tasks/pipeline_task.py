from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["PipelineTask", "PipelineTaskParam"]


@dataclass(kw_only=True)
class PipelineTask:
    """"""

    pipeline_id: VariableOr[str]
    """
    The full name of the pipeline task to execute.
    """

    full_refresh: VariableOrOptional[bool] = None
    """
    If true, triggers a full refresh on the delta live table.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        pipeline_id: VariableOr[str],
        full_refresh: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class PipelineTaskDict(TypedDict, total=False):
    """"""

    pipeline_id: VariableOr[str]
    """
    The full name of the pipeline task to execute.
    """

    full_refresh: VariableOrOptional[bool]
    """
    If true, triggers a full refresh on the delta live table.
    """


PipelineTaskParam = PipelineTaskDict | PipelineTask
