from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SparkSubmitTask", "SparkSubmitTaskParam"]


@dataclass(kw_only=True)
class SparkSubmitTask:
    """"""

    parameters: VariableOrList[str] = field(default_factory=list)
    """
    Command-line parameters passed to spark submit.
    
    Use [Task parameter variables](https://docs.databricks.com/jobs.html#parameter-variables) to set parameters containing information about job runs.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        parameters: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SparkSubmitTaskDict(TypedDict, total=False):
    """"""

    parameters: VariableOrList[str]
    """
    Command-line parameters passed to spark submit.
    
    Use [Task parameter variables](https://docs.databricks.com/jobs.html#parameter-variables) to set parameters containing information about job runs.
    """


SparkSubmitTaskParam = SparkSubmitTaskDict | SparkSubmitTask
