from enum import Enum
from typing import Literal

__all__ = ["AwsAvailability", "AwsAvailabilityParam"]


class AwsAvailability(Enum):
    SPOT = "SPOT"
    ON_DEMAND = "ON_DEMAND"
    SPOT_WITH_FALLBACK = "SPOT_WITH_FALLBACK"


AwsAvailabilityParam = (
    Literal["SPOT", "ON_DEMAND", "SPOT_WITH_FALLBACK"] | AwsAvailability
)
