import inspect
from dataclasses import dataclass, is_dataclass
from enum import Enum
from typing import Any, Callable, Optional

from databricks.bundles.internal._transform import (
    _unwrap_dict,
    _unwrap_list,
    _unwrap_optional,
)


@dataclass
class ParameterSignature:
    tpe: type | Any
    has_default_value: bool
    default_value: Any


class Inspections:
    _SUPPORTED_TYPES = [int, float, str, bool]
    _SUPPORTED_TYPE_NAMES = [
        "int",
        "str",
        "float",
        "bool",
        "list[<type>]",
        "Optional[<type>]",
        "dict[str, <type>]",
        "<enum>",
        "<dataclass>",
    ]

    @staticmethod
    def get_resource_name(function: Callable) -> str:
        return Inspections.get_full_name(function).replace(":", "_").replace(".", "_")

    @staticmethod
    def get_simple_name(function: Callable) -> str:
        return function.__name__

    @staticmethod
    def get_task_func_name(function: Callable) -> str:
        """
        Returns a stable name for task_function in PythonTask.
        """

        return Inspections.get_full_name(function)

    @staticmethod
    def get_full_name(function: Callable) -> str:
        module = inspect.getmodule(function)

        if module and module.__name__ != "__main__":
            return f"{module.__name__}:{function.__name__}"
        else:
            return function.__name__

    @staticmethod
    def get_return_type(function: Callable) -> dict[str, type]:
        signature = inspect.signature(function)
        return_annotation = signature.return_annotation

        if return_annotation == inspect.Parameter.empty:
            return {}

        if return_annotation is None:
            return {}

        if not Inspections.is_supported_type(return_annotation):
            name = Inspections.get_full_name(function)

            display_name = (
                return_annotation.__name__
                if hasattr(return_annotation, "__name__")
                else repr(return_annotation)
            )

            raise ValueError(
                f"'{name}' has unsupported return type: '{display_name}', "
                f"supported types are: {', '.join(Inspections._SUPPORTED_TYPE_NAMES)}"
            )

        return {"return_value": return_annotation}

    @staticmethod
    def get_parameters(function: Callable) -> dict[str, type]:
        return {
            key: signature.tpe
            for key, signature in Inspections.get_parameter_signatures(function).items()
        }

    @staticmethod
    def get_parameter_signatures(function: Callable) -> dict[str, ParameterSignature]:
        signature = inspect.signature(function)
        parameters = dict[str, ParameterSignature]()

        for param in signature.parameters.values():
            if param.annotation == inspect.Parameter.empty:
                name = Inspections.get_full_name(function)
                raise ValueError(
                    f"Parameter '{param.name}' in '{name}' "
                    f"doesn't have type annotation"
                )

            if not Inspections.is_supported_type(param.annotation):
                name = Inspections.get_full_name(function)
                raise ValueError(
                    f"Parameter '{param.name}' in '{name}' has unsupported type "
                    f"'{param.annotation.__name__}' supported types are: "
                    f"{', '.join(Inspections._SUPPORTED_TYPE_NAMES)}"
                )

            if param.default == inspect.Parameter.empty:
                default_value = None
                has_default_value = False
            else:
                default_value = param.default
                has_default_value = True

            parameters[param.name] = ParameterSignature(
                tpe=param.annotation,
                default_value=default_value,
                has_default_value=has_default_value,
            )

        return parameters

    @staticmethod
    def to_named_parameters(
        function: Callable, args: tuple[Any, ...], kwargs: dict
    ) -> dict:
        signature = inspect.signature(function)
        ordered = {}

        unordered = signature.bind(*args, **kwargs).arguments

        for param in signature.parameters.keys():
            if param in unordered:
                ordered[param] = unordered[param]

        return ordered

    @classmethod
    def is_supported_type(cls, tpe: type) -> bool:
        if arg := _unwrap_optional(tpe):
            return cls.is_supported_type(arg)

        if arg := _unwrap_list(tpe):
            return cls.is_supported_type(arg)

        if arg := _unwrap_dict(tpe):
            (key_arg, value_arg) = arg

            if key_arg != str:
                return False

            return cls.is_supported_type(value_arg)

        if is_dataclass(tpe):
            return True

        if isinstance(tpe, type) and issubclass(tpe, Enum):
            return True

        return tpe in Inspections._SUPPORTED_TYPES

    @staticmethod
    def get_closure_vars(function: Callable) -> dict:
        return dict(inspect.getclosurevars(function).globals)

    @staticmethod
    def get_closure_nonlocal_vars(function: Callable) -> dict:
        return dict(inspect.getclosurevars(function).nonlocals)

    @staticmethod
    def get_docstring(function: Callable) -> Optional[str]:
        return inspect.getdoc(function)
