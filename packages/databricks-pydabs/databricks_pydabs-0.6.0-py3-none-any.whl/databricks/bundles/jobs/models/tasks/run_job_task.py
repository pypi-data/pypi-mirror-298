from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrDict

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["RunJobTask", "RunJobTaskParam"]


@dataclass(kw_only=True)
class RunJobTask:
    """"""

    job_id: VariableOr[int]
    """
    ID of the job to trigger.
    """

    job_parameters: VariableOrDict[str] = field(default_factory=dict)
    """
    Job-level parameters used to trigger the job.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        job_id: VariableOr[int],
        job_parameters: Optional[VariableOrDict[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class RunJobTaskDict(TypedDict, total=False):
    """"""

    job_id: VariableOr[int]
    """
    ID of the job to trigger.
    """

    job_parameters: VariableOrDict[str]
    """
    Job-level parameters used to trigger the job.
    """


RunJobTaskParam = RunJobTaskDict | RunJobTask
