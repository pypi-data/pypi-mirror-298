from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["Environment", "EnvironmentParam"]


@dataclass(kw_only=True)
class Environment:
    """"""

    client: VariableOr[str]
    """
    Client version used by the environment
    The client is the user-facing environment of the runtime.
    Each client comes with a specific set of pre-installed libraries.
    The version is a string, consisting of the major client version.
    """

    dependencies: VariableOrList[str] = field(default_factory=list)
    """
    List of pip dependencies, as supported by the version of pip in this environment.
    Each dependency is a pip requirement file line https://pip.pypa.io/en/stable/reference/requirements-file-format/
    Allowed dependency could be <requirement specifier>, <archive url/path>, <local project path>(WSFS or Volumes in Databricks), <vcs project url>
    E.g. dependencies: ["foo==0.0.1", "-r /Workspace/test/requirements.txt"]
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        client: VariableOr[str],
        dependencies: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class EnvironmentDict(TypedDict, total=False):
    """"""

    client: VariableOr[str]
    """
    Client version used by the environment
    The client is the user-facing environment of the runtime.
    Each client comes with a specific set of pre-installed libraries.
    The version is a string, consisting of the major client version.
    """

    dependencies: VariableOrList[str]
    """
    List of pip dependencies, as supported by the version of pip in this environment.
    Each dependency is a pip requirement file line https://pip.pypa.io/en/stable/reference/requirements-file-format/
    Allowed dependency could be <requirement specifier>, <archive url/path>, <local project path>(WSFS or Volumes in Databricks), <vcs project url>
    E.g. dependencies: ["foo==0.0.1", "-r /Workspace/test/requirements.txt"]
    """


EnvironmentParam = EnvironmentDict | Environment
