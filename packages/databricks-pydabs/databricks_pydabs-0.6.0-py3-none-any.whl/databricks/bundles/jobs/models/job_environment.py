from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.compute.models.environment import Environment, EnvironmentParam
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["JobEnvironment", "JobEnvironmentParam"]


@dataclass(kw_only=True)
class JobEnvironment:
    """"""

    environment_key: VariableOr[str]
    """
    The key of an environment. It has to be unique within a job.
    """

    spec: VariableOrOptional[Environment] = None

    @classmethod
    def create(
        cls,
        /,
        *,
        environment_key: VariableOr[str],
        spec: VariableOrOptional[EnvironmentParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobEnvironmentDict(TypedDict, total=False):
    """"""

    environment_key: VariableOr[str]
    """
    The key of an environment. It has to be unique within a job.
    """

    spec: VariableOrOptional[EnvironmentParam]


JobEnvironmentParam = JobEnvironmentDict | JobEnvironment
