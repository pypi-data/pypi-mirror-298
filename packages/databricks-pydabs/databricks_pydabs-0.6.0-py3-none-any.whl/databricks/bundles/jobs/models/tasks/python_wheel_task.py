from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.variables import VariableOr, VariableOrDict, VariableOrList

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ["PythonWheelTask", "PythonWheelTaskParam"]


@dataclass(kw_only=True)
class PythonWheelTask:
    """"""

    entry_point: VariableOr[str]
    """
    Named entry point to use, if it does not exist in the metadata of the package it executes the function from the package directly using `$packageName.$entryPoint()`
    """

    package_name: VariableOr[str]
    """
    Name of the package to execute
    """

    named_parameters: VariableOrDict[str] = field(default_factory=dict)
    """
    Command-line parameters passed to Python wheel task in the form of `["--name=task", "--data=dbfs:/path/to/data.json"]`. Leave it empty if `parameters` is not null.
    """

    parameters: VariableOrList[str] = field(default_factory=list)
    """
    Command-line parameters passed to Python wheel task. Leave it empty if `named_parameters` is not null.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        entry_point: VariableOr[str],
        package_name: VariableOr[str],
        named_parameters: Optional[VariableOrDict[str]] = None,
        parameters: Optional[VariableOrList[str]] = None,
    ) -> "Self":
        return _transform(cls, locals())


class PythonWheelTaskDict(TypedDict, total=False):
    """"""

    entry_point: VariableOr[str]
    """
    Named entry point to use, if it does not exist in the metadata of the package it executes the function from the package directly using `$packageName.$entryPoint()`
    """

    package_name: VariableOr[str]
    """
    Name of the package to execute
    """

    named_parameters: VariableOrDict[str]
    """
    Command-line parameters passed to Python wheel task in the form of `["--name=task", "--data=dbfs:/path/to/data.json"]`. Leave it empty if `parameters` is not null.
    """

    parameters: VariableOrList[str]
    """
    Command-line parameters passed to Python wheel task. Leave it empty if `named_parameters` is not null.
    """


PythonWheelTaskParam = PythonWheelTaskDict | PythonWheelTask
