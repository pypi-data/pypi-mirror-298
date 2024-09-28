from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, TypedDict

from databricks.bundles.compute.models.cluster_spec import ClusterSpec, ClusterSpecParam
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["JobCluster", "JobClusterParam"]


@dataclass(kw_only=True)
class JobCluster:
    """"""

    DEFAULT_KEY: ClassVar[str] = "Default"

    job_cluster_key: VariableOr[str]
    """
    A unique name for the job cluster. This field is required and must be unique within the job.
    `JobTaskSettings` may refer to this field to determine which cluster to launch for the task execution.
    """

    new_cluster: VariableOr[ClusterSpec]
    """
    If new_cluster, a description of a cluster that is created for each task.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        job_cluster_key: VariableOr[str],
        new_cluster: VariableOr[ClusterSpecParam],
    ) -> "Self":
        return _transform(cls, locals())


class JobClusterDict(TypedDict, total=False):
    """"""

    job_cluster_key: VariableOr[str]
    """
    A unique name for the job cluster. This field is required and must be unique within the job.
    `JobTaskSettings` may refer to this field to determine which cluster to launch for the task execution.
    """

    new_cluster: VariableOr[ClusterSpecParam]
    """
    If new_cluster, a description of a cluster that is created for each task.
    """


JobClusterParam = JobClusterDict | JobCluster
