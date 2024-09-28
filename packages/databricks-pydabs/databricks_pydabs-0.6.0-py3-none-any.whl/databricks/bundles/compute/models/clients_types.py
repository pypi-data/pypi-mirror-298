from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["ClientsTypes", "ClientsTypesParam"]


@dataclass(kw_only=True)
class ClientsTypes:
    """"""

    jobs: VariableOrOptional[bool] = None
    """
    With jobs set, the cluster can be used for jobs
    """

    notebooks: VariableOrOptional[bool] = None
    """
    With notebooks set, this cluster can be used for notebooks
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        jobs: VariableOrOptional[bool] = None,
        notebooks: VariableOrOptional[bool] = None,
    ) -> "Self":
        return _transform(cls, locals())


class ClientsTypesDict(TypedDict, total=False):
    """"""

    jobs: VariableOrOptional[bool]
    """
    With jobs set, the cluster can be used for jobs
    """

    notebooks: VariableOrOptional[bool]
    """
    With notebooks set, this cluster can be used for notebooks
    """


ClientsTypesParam = ClientsTypesDict | ClientsTypes
