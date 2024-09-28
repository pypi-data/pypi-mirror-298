from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["GcsStorageInfo", "GcsStorageInfoParam"]


@dataclass(kw_only=True)
class GcsStorageInfo:
    """"""

    destination: VariableOr[str]
    """
    GCS destination/URI, e.g. `gs://my-bucket/some-prefix`
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        destination: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class GcsStorageInfoDict(TypedDict, total=False):
    """"""

    destination: VariableOr[str]
    """
    GCS destination/URI, e.g. `gs://my-bucket/some-prefix`
    """


GcsStorageInfoParam = GcsStorageInfoDict | GcsStorageInfo
