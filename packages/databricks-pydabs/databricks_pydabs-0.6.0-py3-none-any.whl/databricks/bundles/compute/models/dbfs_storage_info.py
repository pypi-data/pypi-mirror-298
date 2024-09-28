from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["DbfsStorageInfo", "DbfsStorageInfoParam"]


@dataclass(kw_only=True)
class DbfsStorageInfo:
    """"""

    destination: VariableOr[str]
    """
    dbfs destination, e.g. `dbfs:/my/path`
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        destination: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class DbfsStorageInfoDict(TypedDict, total=False):
    """"""

    destination: VariableOr[str]
    """
    dbfs destination, e.g. `dbfs:/my/path`
    """


DbfsStorageInfoParam = DbfsStorageInfoDict | DbfsStorageInfo
