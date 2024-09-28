from enum import Enum
from typing import Literal

__all__ = ["Source", "SourceParam"]


class Source(Enum):
    WORKSPACE = "WORKSPACE"
    GIT = "GIT"


SourceParam = Literal["WORKSPACE", "GIT"] | Source
