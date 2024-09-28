from enum import Enum
from typing import Literal

__all__ = ["DataSecurityMode", "DataSecurityModeParam"]


class DataSecurityMode(Enum):
    NONE = "NONE"
    SINGLE_USER = "SINGLE_USER"
    USER_ISOLATION = "USER_ISOLATION"
    LEGACY_TABLE_ACL = "LEGACY_TABLE_ACL"
    LEGACY_PASSTHROUGH = "LEGACY_PASSTHROUGH"
    LEGACY_SINGLE_USER = "LEGACY_SINGLE_USER"
    LEGACY_SINGLE_USER_STANDARD = "LEGACY_SINGLE_USER_STANDARD"


DataSecurityModeParam = (
    Literal[
        "NONE",
        "SINGLE_USER",
        "USER_ISOLATION",
        "LEGACY_TABLE_ACL",
        "LEGACY_PASSTHROUGH",
        "LEGACY_SINGLE_USER",
        "LEGACY_SINGLE_USER_STANDARD",
    ]
    | DataSecurityMode
)
