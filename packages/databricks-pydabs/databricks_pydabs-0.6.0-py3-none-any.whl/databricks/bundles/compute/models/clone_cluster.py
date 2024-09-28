from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["CloneCluster", "CloneClusterParam"]


@dataclass(kw_only=True)
class CloneCluster:
    """"""

    source_cluster_id: VariableOr[str]
    """
    The cluster that is being cloned.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        source_cluster_id: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class CloneClusterDict(TypedDict, total=False):
    """"""

    source_cluster_id: VariableOr[str]
    """
    The cluster that is being cloned.
    """


CloneClusterParam = CloneClusterDict | CloneCluster
