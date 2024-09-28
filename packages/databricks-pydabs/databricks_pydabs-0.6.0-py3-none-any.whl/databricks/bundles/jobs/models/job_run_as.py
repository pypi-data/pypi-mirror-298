from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["JobRunAs", "JobRunAsParam"]


@dataclass(kw_only=True)
class JobRunAs:
    """"""

    user_name: VariableOrOptional[str] = None
    """
    The email of an active workspace user. Non-admin users can only set this field to their own email.
    """

    service_principal_name: VariableOrOptional[str] = None
    """
    Application ID of an active service principal. Setting this field requires the `servicePrincipal/user` role.
    """

    def __post_init__(self):
        union_fields = [
            self.user_name,
            self.service_principal_name,
        ]

        if sum(f is not None for f in union_fields) != 1:
            raise ValueError(
                "JobRunAs must specify exactly one of 'user_name', 'service_principal_name'"
            )

    @classmethod
    def create(
        cls,
        /,
        *,
        user_name: VariableOrOptional[str] = None,
        service_principal_name: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class JobRunAsDict(TypedDict, total=False):
    """"""

    user_name: VariableOrOptional[str]
    """
    The email of an active workspace user. Non-admin users can only set this field to their own email.
    """

    service_principal_name: VariableOrOptional[str]
    """
    Application ID of an active service principal. Setting this field requires the `servicePrincipal/user` role.
    """


JobRunAsParam = JobRunAsDict | JobRunAs
