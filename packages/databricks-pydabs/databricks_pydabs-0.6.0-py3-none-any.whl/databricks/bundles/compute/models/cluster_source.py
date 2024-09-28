from enum import Enum
from typing import Literal

__all__ = ["ClusterSource", "ClusterSourceParam"]


class ClusterSource(Enum):
    UI = "UI"
    JOB = "JOB"
    API = "API"
    SQL = "SQL"
    MODELS = "MODELS"
    PIPELINE = "PIPELINE"
    PIPELINE_MAINTENANCE = "PIPELINE_MAINTENANCE"


ClusterSourceParam = (
    Literal["UI", "JOB", "API", "SQL", "MODELS", "PIPELINE", "PIPELINE_MAINTENANCE"]
    | ClusterSource
)
