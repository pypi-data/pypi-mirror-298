from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["QueueSettings", "QueueSettingsParam"]


@dataclass(kw_only=True)
class QueueSettings:
    """"""

    enabled: VariableOr[bool]
    """
    If true, enable queueing for the job. This is a required field.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        enabled: VariableOr[bool],
    ) -> "Self":
        return _transform(cls, locals())


class QueueSettingsDict(TypedDict, total=False):
    """"""

    enabled: VariableOr[bool]
    """
    If true, enable queueing for the job. This is a required field.
    """


QueueSettingsParam = QueueSettingsDict | QueueSettings
