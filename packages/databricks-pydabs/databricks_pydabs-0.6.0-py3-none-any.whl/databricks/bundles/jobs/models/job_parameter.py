from dataclasses import dataclass
from typing import TYPE_CHECKING, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["JobParameterDefinition", "JobParameterDefinitionParam"]


@dataclass(kw_only=True)
class JobParameterDefinition:
    """"""

    default: VariableOr[str]
    """
    Default value of the parameter.
    """

    name: VariableOr[str]
    """
    The name of the defined parameter. May only contain alphanumeric characters, `_`, `-`, and `.`
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        default: VariableOr[str],
        name: VariableOr[str],
    ) -> "Self":
        return _transform(cls, locals())


class JobParameterDefinitionDict(TypedDict, total=False):
    """"""

    default: VariableOr[str]
    """
    Default value of the parameter.
    """

    name: VariableOr[str]
    """
    The name of the defined parameter. May only contain alphanumeric characters, `_`, `-`, and `.`
    """


JobParameterDefinitionParam = JobParameterDefinitionDict | JobParameterDefinition
