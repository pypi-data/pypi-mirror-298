from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["VolumesStorageInfo", "VolumesStorageInfoParam"]


@dataclass(kw_only=True)
class VolumesStorageInfo:
    """"""

    destination: VariableOr[str]
    """
    Unity Catalog Volumes file destination, e.g. `/Volumes/my-init.sh`
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        destination: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class VolumesStorageInfoDict(TypedDict, total=False):
    """"""

    destination: VariableOr[str]
    """
    Unity Catalog Volumes file destination, e.g. `/Volumes/my-init.sh`
    """


VolumesStorageInfoParam = VolumesStorageInfoDict | VolumesStorageInfo
