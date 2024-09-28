from enum import Enum
from typing import Literal

__all__ = ["PauseStatus", "PauseStatusParam"]


class PauseStatus(Enum):
    UNPAUSED = "UNPAUSED"
    PAUSED = "PAUSED"


PauseStatusParam = Literal["UNPAUSED", "PAUSED"] | PauseStatus
