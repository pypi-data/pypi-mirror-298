from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.compute.models.docker_basic_auth import (
    DockerBasicAuth,
    DockerBasicAuthParam,
)
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["DockerImage", "DockerImageParam"]


@dataclass(kw_only=True)
class DockerImage:
    """"""

    basic_auth: VariableOrOptional[DockerBasicAuth] = None

    url: VariableOrOptional[str] = None
    """
    URL of the docker image.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        basic_auth: VariableOrOptional[DockerBasicAuthParam] = None,
        url: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class DockerImageDict(TypedDict, total=False):
    """"""

    basic_auth: VariableOrOptional[DockerBasicAuthParam]

    url: VariableOrOptional[str]
    """
    URL of the docker image.
    """


DockerImageParam = DockerImageDict | DockerImage
