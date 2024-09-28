from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["AutoScale", "AutoScaleParam"]


@dataclass(kw_only=True)
class AutoScale:
    """"""

    max_workers: VariableOrOptional[int] = None
    """
    The maximum number of workers to which the cluster can scale up when overloaded.
    Note that `max_workers` must be strictly greater than `min_workers`.
    """

    min_workers: VariableOrOptional[int] = None
    """
    The minimum number of workers to which the cluster can scale down when underutilized.
    It is also the initial number of workers the cluster will have after creation.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        max_workers: VariableOrOptional[int] = None,
        min_workers: VariableOrOptional[int] = None,
    ) -> "Self":
        return _transform(cls, locals())


class AutoScaleDict(TypedDict, total=False):
    """"""

    max_workers: VariableOrOptional[int]
    """
    The maximum number of workers to which the cluster can scale up when overloaded.
    Note that `max_workers` must be strictly greater than `min_workers`.
    """

    min_workers: VariableOrOptional[int]
    """
    The minimum number of workers to which the cluster can scale down when underutilized.
    It is also the initial number of workers the cluster will have after creation.
    """


AutoScaleParam = AutoScaleDict | AutoScale
