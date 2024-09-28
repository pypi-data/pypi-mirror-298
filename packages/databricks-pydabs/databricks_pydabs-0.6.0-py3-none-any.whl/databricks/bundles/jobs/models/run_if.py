from enum import Enum
from typing import Literal

__all__ = ["RunIf", "RunIfParam"]


class RunIf(Enum):
    ALL_SUCCESS = "ALL_SUCCESS"
    ALL_DONE = "ALL_DONE"
    NONE_FAILED = "NONE_FAILED"
    AT_LEAST_ONE_SUCCESS = "AT_LEAST_ONE_SUCCESS"
    ALL_FAILED = "ALL_FAILED"
    AT_LEAST_ONE_FAILED = "AT_LEAST_ONE_FAILED"


RunIfParam = (
    Literal[
        "ALL_SUCCESS",
        "ALL_DONE",
        "NONE_FAILED",
        "AT_LEAST_ONE_SUCCESS",
        "ALL_FAILED",
        "AT_LEAST_ONE_FAILED",
    ]
    | RunIf
)
