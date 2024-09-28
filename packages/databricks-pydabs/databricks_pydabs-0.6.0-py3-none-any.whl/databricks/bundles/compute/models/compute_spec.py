from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["ComputeSpec"]


@dataclass(kw_only=True)
class ComputeSpec:
    """"""

    """
    The kind of compute described by this compute specification.
    """
    kind: Optional[str] = None

    @classmethod
    def create(
        cls,
        /,
        *,
        kind: Optional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class ComputeSpecDict(TypedDict, total=False):
    """"""

    """
    The kind of compute described by this compute specification.
    """
    kind: Optional[str]


ComputeSpecParam = ComputeSpecDict | ComputeSpec
