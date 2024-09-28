from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["SqlTaskSubscription", "SqlTaskSubscriptionParam"]


@dataclass(kw_only=True)
class SqlTaskSubscription:
    """"""

    destination_id: VariableOrOptional[str] = None
    """
    The canonical identifier of the destination to receive email notification. This parameter is mutually exclusive with user_name. You cannot set both destination_id and user_name for subscription notifications.
    """

    user_name: VariableOrOptional[str] = None
    """
    The user name to receive the subscription email. This parameter is mutually exclusive with destination_id. You cannot set both destination_id and user_name for subscription notifications.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        destination_id: VariableOrOptional[str] = None,
        user_name: VariableOrOptional[str] = None,
    ) -> "Self":
        return _transform(cls, locals())


class SqlTaskSubscriptionDict(TypedDict, total=False):
    """"""

    destination_id: VariableOrOptional[str]
    """
    The canonical identifier of the destination to receive email notification. This parameter is mutually exclusive with user_name. You cannot set both destination_id and user_name for subscription notifications.
    """

    user_name: VariableOrOptional[str]
    """
    The user name to receive the subscription email. This parameter is mutually exclusive with destination_id. You cannot set both destination_id and user_name for subscription notifications.
    """


SqlTaskSubscriptionParam = SqlTaskSubscriptionDict | SqlTaskSubscription
