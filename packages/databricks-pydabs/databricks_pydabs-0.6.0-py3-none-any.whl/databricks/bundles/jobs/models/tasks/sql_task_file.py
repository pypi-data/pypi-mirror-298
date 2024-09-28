from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.source import Source, SourceParam
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTaskFile", "SqlTaskFileParam"]


@dataclass(kw_only=True)
class SqlTaskFile:
    """"""

    path: VariableOr[str]
    """
    Path of the SQL file. Must be relative if the source is a remote Git repository and absolute for workspace paths.
    """

    source: VariableOrOptional[Source] = None
    """
    Optional location type of the SQL file. When set to `WORKSPACE`, the SQL file will be retrieved
    from the local Databricks workspace. When set to `GIT`, the SQL file will be retrieved from a Git repository
    defined in `git_source`. If the value is empty, the task will use `GIT` if `git_source` is defined and `WORKSPACE` otherwise.
    
    * `WORKSPACE`: SQL file is located in Databricks workspace.
    * `GIT`: SQL file is located in cloud Git provider.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        path: VariableOr[str],
        source: VariableOrOptional[SourceParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskFileDict(TypedDict, total=False):
    """"""

    path: VariableOr[str]
    """
    Path of the SQL file. Must be relative if the source is a remote Git repository and absolute for workspace paths.
    """

    source: VariableOrOptional[SourceParam]
    """
    Optional location type of the SQL file. When set to `WORKSPACE`, the SQL file will be retrieved
    from the local Databricks workspace. When set to `GIT`, the SQL file will be retrieved from a Git repository
    defined in `git_source`. If the value is empty, the task will use `GIT` if `git_source` is defined and `WORKSPACE` otherwise.
    
    * `WORKSPACE`: SQL file is located in Databricks workspace.
    * `GIT`: SQL file is located in cloud Git provider.
    """


SqlTaskFileParam = SqlTaskFileDict | SqlTaskFile
