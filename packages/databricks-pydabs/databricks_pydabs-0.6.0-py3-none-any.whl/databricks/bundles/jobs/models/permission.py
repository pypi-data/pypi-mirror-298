from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Literal, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["PermissionLevel", "PermissionLevelParam", "Permission", "PermissionParam"]


class PermissionLevel(Enum):
    IS_OWNER = "IS_OWNER"
    CAN_MANAGE = "CAN_MANAGE"
    CAN_MANAGE_RUN = "CAN_MANAGE_RUN"
    CAN_VIEW = "CAN_VIEW"


PermissionLevelParam = (
    Literal["IS_OWNER", "CAN_MANAGE", "CAN_MANAGE_RUN", "CAN_VIEW"] | PermissionLevel
)


@dataclass(kw_only=True)
class Permission:
    """"""

    level: VariableOr[PermissionLevel]

    user_name: VariableOrOptional[str] = None

    service_principal_name: VariableOrOptional[str] = None

    group_name: VariableOrOptional[str] = None

    def __post_init__(self):
        union_fields = [
            self.user_name,
            self.service_principal_name,
            self.group_name,
        ]

        if sum(f is not None for f in union_fields) != 1:
            raise ValueError(
                "Permission must specify exactly one of 'user_name', 'service_principal_name', 'group_name'"
            )

    @classmethod
    def create(
        cls,
        /,
        *,
        level: VariableOr[PermissionLevelParam],
        user_name: VariableOrOptional[str] = None,
        service_principal_name: VariableOrOptional[str] = None,
        group_name: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class PermissionDict(TypedDict, total=False):
    """"""

    level: VariableOr[PermissionLevelParam]

    user_name: VariableOrOptional[str]

    service_principal_name: VariableOrOptional[str]

    group_name: VariableOrOptional[str]


PermissionParam = PermissionDict | Permission
