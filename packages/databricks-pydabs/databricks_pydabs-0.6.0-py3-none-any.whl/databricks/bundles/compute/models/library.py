from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "RCranLibrary",
    "RCranLibraryParam",
    "MavenLibrary",
    "MavenLibraryParam",
    "PythonPyPiLibrary",
    "PythonPyPiLibraryParam",
    "Library",
    "LibraryParam",
]


@dataclass(kw_only=True)
class RCranLibrary:
    """"""

    package: VariableOr[str]
    """
    The name of the CRAN package to install.
    """

    repo: VariableOrOptional[str] = None
    """
    The repository where the package can be found. If not specified, the default CRAN repo is used.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        package: VariableOr[str],
        repo: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class RCranLibraryDict(TypedDict, total=False):
    """"""

    package: VariableOr[str]
    """
    The name of the CRAN package to install.
    """

    repo: VariableOrOptional[str]
    """
    The repository where the package can be found. If not specified, the default CRAN repo is used.
    """


RCranLibraryParam = RCranLibraryDict | RCranLibrary


@dataclass(kw_only=True)
class MavenLibrary:
    """"""

    coordinates: VariableOr[str]
    """
    Gradle-style maven coordinates. For example: "org.jsoup:jsoup:1.7.2".
    """

    exclusions: VariableOrList[str] = field(default_factory=list)
    """
    List of dependences to exclude. For example: `["slf4j:slf4j", "*:hadoop-client"]`.
    
    Maven dependency exclusions:
    https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html.
    """

    repo: VariableOrOptional[str] = None
    """
    Maven repo to install the Maven package from. If omitted, both Maven Central Repository
    and Spark Packages are searched.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        coordinates: VariableOr[str],
        exclusions: Optional[VariableOrList[str]] = None,
        repo: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class MavenLibraryDict(TypedDict, total=False):
    """"""

    coordinates: VariableOr[str]
    """
    Gradle-style maven coordinates. For example: "org.jsoup:jsoup:1.7.2".
    """

    exclusions: VariableOrList[str]
    """
    List of dependences to exclude. For example: `["slf4j:slf4j", "*:hadoop-client"]`.
    
    Maven dependency exclusions:
    https://maven.apache.org/guides/introduction/introduction-to-optional-and-excludes-dependencies.html.
    """

    repo: VariableOrOptional[str]
    """
    Maven repo to install the Maven package from. If omitted, both Maven Central Repository
    and Spark Packages are searched.
    """


MavenLibraryParam = MavenLibraryDict | MavenLibrary


@dataclass(kw_only=True)
class PythonPyPiLibrary:
    """"""

    package: VariableOr[str]
    """
    The name of the pypi package to install. An optional exact version specification is also
    supported. Examples: "simplejson" and "simplejson==3.8.0".
    """

    repo: VariableOrOptional[str] = None
    """
    The repository where the package can be found. If not specified, the default pip index is
    used.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        package: VariableOr[str],
        repo: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class PythonPyPiLibraryDict(TypedDict, total=False):
    """"""

    package: VariableOr[str]
    """
    The name of the pypi package to install. An optional exact version specification is also
    supported. Examples: "simplejson" and "simplejson==3.8.0".
    """

    repo: VariableOrOptional[str]
    """
    The repository where the package can be found. If not specified, the default pip index is
    used.
    """


PythonPyPiLibraryParam = PythonPyPiLibraryDict | PythonPyPiLibrary


@dataclass(kw_only=True)
class Library:
    """"""

    cran: VariableOrOptional[RCranLibrary] = None
    """
    Specification of a CRAN library to be installed as part of the library
    """

    egg: VariableOrOptional[str] = None
    """
    URI of the egg library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "egg": "/Workspace/path/to/library.egg" }`, `{ "egg" : "/Volumes/path/to/library.egg" }` or
    `{ "egg": "s3://my-bucket/library.egg" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """

    jar: VariableOrOptional[str] = None
    """
    URI of the JAR library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "jar": "/Workspace/path/to/library.jar" }`, `{ "jar" : "/Volumes/path/to/library.jar" }` or
    `{ "jar": "s3://my-bucket/library.jar" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """

    maven: VariableOrOptional[MavenLibrary] = None
    """
    Specification of a maven library to be installed. For example:
    `{ "coordinates": "org.jsoup:jsoup:1.7.2" }`
    """

    pypi: VariableOrOptional[PythonPyPiLibrary] = None
    """
    Specification of a PyPi library to be installed. For example:
    `{ "package": "simplejson" }`
    """

    requirements: VariableOrOptional[str] = None
    """
    URI of the requirements.txt file to install. Only Workspace paths and Unity Catalog Volumes paths are supported.
    For example: `{ "requirements": "/Workspace/path/to/requirements.txt" }` or `{ "requirements" : "/Volumes/path/to/requirements.txt" }`
    """

    whl: VariableOrOptional[str] = None
    """
    URI of the wheel library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "whl": "/Workspace/path/to/library.whl" }`, `{ "whl" : "/Volumes/path/to/library.whl" }` or
    `{ "whl": "s3://my-bucket/library.whl" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        cran: VariableOrOptional[RCranLibraryParam] = None,
        egg: VariableOrOptional[str] = None,
        jar: VariableOrOptional[str] = None,
        maven: VariableOrOptional[MavenLibraryParam] = None,
        pypi: VariableOrOptional[PythonPyPiLibraryParam] = None,
        requirements: VariableOrOptional[str] = None,
        whl: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class LibraryDict(TypedDict, total=False):
    """"""

    cran: VariableOrOptional[RCranLibraryParam]
    """
    Specification of a CRAN library to be installed as part of the library
    """

    egg: VariableOrOptional[str]
    """
    URI of the egg library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "egg": "/Workspace/path/to/library.egg" }`, `{ "egg" : "/Volumes/path/to/library.egg" }` or
    `{ "egg": "s3://my-bucket/library.egg" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """

    jar: VariableOrOptional[str]
    """
    URI of the JAR library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "jar": "/Workspace/path/to/library.jar" }`, `{ "jar" : "/Volumes/path/to/library.jar" }` or
    `{ "jar": "s3://my-bucket/library.jar" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """

    maven: VariableOrOptional[MavenLibraryParam]
    """
    Specification of a maven library to be installed. For example:
    `{ "coordinates": "org.jsoup:jsoup:1.7.2" }`
    """

    pypi: VariableOrOptional[PythonPyPiLibraryParam]
    """
    Specification of a PyPi library to be installed. For example:
    `{ "package": "simplejson" }`
    """

    requirements: VariableOrOptional[str]
    """
    URI of the requirements.txt file to install. Only Workspace paths and Unity Catalog Volumes paths are supported.
    For example: `{ "requirements": "/Workspace/path/to/requirements.txt" }` or `{ "requirements" : "/Volumes/path/to/requirements.txt" }`
    """

    whl: VariableOrOptional[str]
    """
    URI of the wheel library to install. Supported URIs include Workspace paths, Unity Catalog Volumes paths, and S3 URIs.
    For example: `{ "whl": "/Workspace/path/to/library.whl" }`, `{ "whl" : "/Volumes/path/to/library.whl" }` or
    `{ "whl": "s3://my-bucket/library.whl" }`.
    If S3 is used, please make sure the cluster has read access on the library. You may need to
    launch the cluster with an IAM role to access the S3 URI.
    """


LibraryParam = LibraryDict | Library
