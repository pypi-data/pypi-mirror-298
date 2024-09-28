from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.compute.models.dbfs_storage_info import (
    DbfsStorageInfo,
    DbfsStorageInfoParam,
)
from databricks.bundles.compute.models.s3_storage_info import (
    S3StorageInfo,
    S3StorageInfoParam,
)
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["ClusterLogConf", "ClusterLogConfParam"]


@dataclass(kw_only=True)
class ClusterLogConf:
    """"""

    dbfs: VariableOrOptional[DbfsStorageInfo] = None
    """
    destination needs to be provided. e.g.
    `{ "dbfs" : { "destination" : "dbfs:/home/cluster_log" } }`
    """

    s3: VariableOrOptional[S3StorageInfo] = None
    """
    destination and either the region or endpoint need to be provided. e.g.
    `{ "s3": { "destination" : "s3://cluster_log_bucket/prefix", "region" : "us-west-2" } }`
    Cluster iam role is used to access s3, please make sure the cluster iam role in
    `instance_profile_arn` has permission to write data to the s3 destination.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        dbfs: VariableOrOptional[DbfsStorageInfoParam] = None,
        s3: VariableOrOptional[S3StorageInfoParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class ClusterLogConfDict(TypedDict, total=False):
    """"""

    dbfs: VariableOrOptional[DbfsStorageInfoParam]
    """
    destination needs to be provided. e.g.
    `{ "dbfs" : { "destination" : "dbfs:/home/cluster_log" } }`
    """

    s3: VariableOrOptional[S3StorageInfoParam]
    """
    destination and either the region or endpoint need to be provided. e.g.
    `{ "s3": { "destination" : "s3://cluster_log_bucket/prefix", "region" : "us-west-2" } }`
    Cluster iam role is used to access s3, please make sure the cluster iam role in
    `instance_profile_arn` has permission to write data to the s3 destination.
    """


ClusterLogConfParam = ClusterLogConfDict | ClusterLogConf
