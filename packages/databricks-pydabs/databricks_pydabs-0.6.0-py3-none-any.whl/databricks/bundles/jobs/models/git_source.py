from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "GitProvider",
    "GitProviderParam",
    "GitSnapshot",
    "GitSnapshotParam",
    "GitSource",
    "GitSourceParam",
]


class GitProvider(Enum):
    GIT_HUB = "gitHub"
    BITBUCKET_CLOUD = "bitbucketCloud"
    AZURE_DEV_OPS_SERVICES = "azureDevOpsServices"
    GIT_HUB_ENTERPRISE = "gitHubEnterprise"
    BITBUCKET_SERVER = "bitbucketServer"
    GIT_LAB = "gitLab"
    GIT_LAB_ENTERPRISE_EDITION = "gitLabEnterpriseEdition"
    AWS_CODE_COMMIT = "awsCodeCommit"


GitProviderParam = (
    Literal[
        "gitHub",
        "bitbucketCloud",
        "azureDevOpsServices",
        "gitHubEnterprise",
        "bitbucketServer",
        "gitLab",
        "gitLabEnterpriseEdition",
        "awsCodeCommit",
    ]
    | GitProvider
)


@dataclass(kw_only=True)
class GitSnapshot:
    """"""

    used_commit: VariableOrOptional[str] = None
    """
    Commit that was used to execute the run. If git_branch was specified, this points to the HEAD of the branch at the time of the run; if git_tag was specified, this points to the commit the tag points to.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        used_commit: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class GitSnapshotDict(TypedDict, total=False):
    """"""

    used_commit: VariableOrOptional[str]
    """
    Commit that was used to execute the run. If git_branch was specified, this points to the HEAD of the branch at the time of the run; if git_tag was specified, this points to the commit the tag points to.
    """


GitSnapshotParam = GitSnapshotDict | GitSnapshot


@dataclass(kw_only=True)
class GitSource:
    """"""

    git_provider: VariableOr[GitProvider]
    """
    Unique identifier of the service used to host the Git repository. The value is case insensitive.
    """

    git_url: VariableOr[str]
    """
    URL of the repository to be cloned by this job.
    """

    git_branch: VariableOrOptional[str] = None
    """
    Name of the branch to be checked out and used by this job. This field cannot be specified in conjunction with git_tag or git_commit.
    """

    git_commit: VariableOrOptional[str] = None
    """
    Commit to be checked out and used by this job. This field cannot be specified in conjunction with git_branch or git_tag.
    """

    git_tag: VariableOrOptional[str] = None
    """
    Name of the tag to be checked out and used by this job. This field cannot be specified in conjunction with git_branch or git_commit.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        git_provider: VariableOr[GitProviderParam],
        git_url: VariableOr[str],
        git_branch: VariableOrOptional[str] = None,
        git_commit: VariableOrOptional[str] = None,
        git_tag: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class GitSourceDict(TypedDict, total=False):
    """"""

    git_provider: VariableOr[GitProviderParam]
    """
    Unique identifier of the service used to host the Git repository. The value is case insensitive.
    """

    git_url: VariableOr[str]
    """
    URL of the repository to be cloned by this job.
    """

    git_branch: VariableOrOptional[str]
    """
    Name of the branch to be checked out and used by this job. This field cannot be specified in conjunction with git_tag or git_commit.
    """

    git_commit: VariableOrOptional[str]
    """
    Commit to be checked out and used by this job. This field cannot be specified in conjunction with git_branch or git_tag.
    """

    git_tag: VariableOrOptional[str]
    """
    Name of the tag to be checked out and used by this job. This field cannot be specified in conjunction with git_branch or git_commit.
    """


GitSourceParam = GitSourceDict | GitSource
