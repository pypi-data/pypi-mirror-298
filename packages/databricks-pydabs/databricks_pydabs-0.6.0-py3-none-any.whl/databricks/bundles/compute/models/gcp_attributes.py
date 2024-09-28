from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.compute.models.gcp_availability import (
    GcpAvailability,
    GcpAvailabilityParam,
)
from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["GcpAttributes", "GcpAttributesParam"]


@dataclass(kw_only=True)
class GcpAttributes:
    """"""

    availability: VariableOrOptional[GcpAvailability] = None

    boot_disk_size: VariableOrOptional[int] = None
    """
    boot disk size in GB
    """

    google_service_account: VariableOrOptional[str] = None
    """
    If provided, the cluster will impersonate the google service account when accessing
    gcloud services (like GCS). The google service account
    must have previously been added to the Databricks environment by an account
    administrator.
    """

    local_ssd_count: VariableOrOptional[int] = None
    """
    If provided, each node (workers and driver) in the cluster will have this number of local SSDs attached. Each local SSD is 375GB in size. Refer to [GCP documentation](https://cloud.google.com/compute/docs/disks/local-ssd#choose_number_local_ssds) for the supported number of local SSDs for each instance type.
    """

    use_preemptible_executors: VariableOrOptional[bool] = None
    """
    This field determines whether the spark executors will be scheduled to run on preemptible VMs (when set to true) versus standard compute engine VMs (when set to false; default).
    Note: Soon to be deprecated, use the availability field instead.
    """

    zone_id: VariableOrOptional[str] = None
    """
    Identifier for the availability zone in which the cluster resides.
    This can be one of the following:
    - "HA" => High availability, spread nodes across availability zones for a Databricks deployment region [default]
    - "AUTO" => Databricks picks an availability zone to schedule the cluster on.
    - A GCP availability zone => Pick One of the available zones for (machine type + region) from https://cloud.google.com/compute/docs/regions-zones.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        availability: VariableOrOptional[GcpAvailabilityParam] = None,
        boot_disk_size: VariableOrOptional[int] = None,
        google_service_account: VariableOrOptional[str] = None,
        local_ssd_count: VariableOrOptional[int] = None,
        use_preemptible_executors: VariableOrOptional[bool] = None,
        zone_id: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class GcpAttributesDict(TypedDict, total=False):
    """"""

    availability: VariableOrOptional[GcpAvailabilityParam]

    boot_disk_size: VariableOrOptional[int]
    """
    boot disk size in GB
    """

    google_service_account: VariableOrOptional[str]
    """
    If provided, the cluster will impersonate the google service account when accessing
    gcloud services (like GCS). The google service account
    must have previously been added to the Databricks environment by an account
    administrator.
    """

    local_ssd_count: VariableOrOptional[int]
    """
    If provided, each node (workers and driver) in the cluster will have this number of local SSDs attached. Each local SSD is 375GB in size. Refer to [GCP documentation](https://cloud.google.com/compute/docs/disks/local-ssd#choose_number_local_ssds) for the supported number of local SSDs for each instance type.
    """

    use_preemptible_executors: VariableOrOptional[bool]
    """
    This field determines whether the spark executors will be scheduled to run on preemptible VMs (when set to true) versus standard compute engine VMs (when set to false; default).
    Note: Soon to be deprecated, use the availability field instead.
    """

    zone_id: VariableOrOptional[str]
    """
    Identifier for the availability zone in which the cluster resides.
    This can be one of the following:
    - "HA" => High availability, spread nodes across availability zones for a Databricks deployment region [default]
    - "AUTO" => Databricks picks an availability zone to schedule the cluster on.
    - A GCP availability zone => Pick One of the available zones for (machine type + region) from https://cloud.google.com/compute/docs/regions-zones.
    """


GcpAttributesParam = GcpAttributesDict | GcpAttributes
