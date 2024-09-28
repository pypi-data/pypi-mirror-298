from enum import Enum
from typing import Literal

__all__ = ["AzureAvailability", "AzureAvailabilityParam"]


class AzureAvailability(Enum):
    SPOT_AZURE = "SPOT_AZURE"
    ON_DEMAND_AZURE = "ON_DEMAND_AZURE"
    SPOT_WITH_FALLBACK_AZURE = "SPOT_WITH_FALLBACK_AZURE"


AzureAvailabilityParam = (
    Literal["SPOT_AZURE", "ON_DEMAND_AZURE", "SPOT_WITH_FALLBACK_AZURE"]
    | AzureAvailability
)
