from enum import Enum
from typing import Literal

__all__ = ["GcpAvailability", "GcpAvailabilityParam"]


class GcpAvailability(Enum):
    PREEMPTIBLE_GCP = "PREEMPTIBLE_GCP"
    ON_DEMAND_GCP = "ON_DEMAND_GCP"
    PREEMPTIBLE_WITH_FALLBACK_GCP = "PREEMPTIBLE_WITH_FALLBACK_GCP"


GcpAvailabilityParam = (
    Literal["PREEMPTIBLE_GCP", "ON_DEMAND_GCP", "PREEMPTIBLE_WITH_FALLBACK_GCP"]
    | GcpAvailability
)
