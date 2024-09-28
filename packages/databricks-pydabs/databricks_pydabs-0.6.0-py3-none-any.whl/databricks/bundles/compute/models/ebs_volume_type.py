from enum import Enum
from typing import Literal

__all__ = ["EbsVolumeType", "EbsVolumeTypeParam"]


class EbsVolumeType(Enum):
    GENERAL_PURPOSE_SSD = "GENERAL_PURPOSE_SSD"
    THROUGHPUT_OPTIMIZED_HDD = "THROUGHPUT_OPTIMIZED_HDD"


EbsVolumeTypeParam = (
    Literal["GENERAL_PURPOSE_SSD", "THROUGHPUT_OPTIMIZED_HDD"] | EbsVolumeType
)
