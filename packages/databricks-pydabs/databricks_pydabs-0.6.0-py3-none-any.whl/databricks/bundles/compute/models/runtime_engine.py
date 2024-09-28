from enum import Enum
from typing import Literal

__all__ = ["RuntimeEngine", "RuntimeEngineParam"]


class RuntimeEngine(Enum):
    NULL = "NULL"
    STANDARD = "STANDARD"
    PHOTON = "PHOTON"


RuntimeEngineParam = Literal["NULL", "STANDARD", "PHOTON"] | RuntimeEngine
