import json
from dataclasses import is_dataclass
from enum import Enum
from typing import Any

from databricks.bundles.internal._transform import (
    _transform,
    _unwrap_dict,
    _unwrap_list,
    _unwrap_optional,
)
from databricks.bundles.internal._transform_to_json import _transform_to_json_value


def _serialize_parameter(tpe: type, value: Any) -> str:
    primitive = _transform_to_json_value(value)

    if isinstance(primitive, str):
        return primitive
    elif isinstance(primitive, bool):
        return "true" if primitive else "false"
    elif isinstance(primitive, int):
        return str(primitive)
    elif primitive is None:
        return ""
    else:
        return json.dumps(primitive)


def _deserialize_parameter(parameter: str, value_type: type) -> Any:
    if arg := _unwrap_optional(value_type):
        if parameter == "":
            return None

        return _deserialize_parameter(parameter, arg)

    if arg := _unwrap_list(value_type):
        return [_transform(arg, item) for item in json.loads(parameter)]

    if arg := _unwrap_dict(value_type):
        [key_arg, value_arg] = arg

        json_value = json.loads(parameter)

        if not isinstance(json_value, dict):
            raise ValueError(f"Expected dict, got {type(json_value)}")

        if key_arg == str:
            return {
                key: _transform(value_arg, value) for key, value in json_value.items()
            }

    if value_type == int:
        return int(parameter)
    elif value_type == str:
        return parameter
    elif value_type == float:
        return float(parameter)
    elif value_type == bool:
        return _transform(bool, parameter)
    elif is_dataclass(value_type):
        return _transform(value_type, json.loads(parameter))
    elif issubclass(value_type, Enum):
        return value_type(parameter)
    else:
        raise ValueError(f"Unsupported parameter type {value_type}")


def _check_parameter_type(value: Any, tpe: type) -> bool:
    if arg := _unwrap_optional(tpe):
        if value is None:
            return True

        return _check_parameter_type(value, arg)

    if arg := _unwrap_list(tpe):
        if not isinstance(value, list):
            return False

        return all(_check_parameter_type(item, arg) for item in value)

    if arg := _unwrap_dict(tpe):
        if not isinstance(value, dict):
            return False

        [key_arg, value_arg] = arg

        return all(
            isinstance(key, key_arg) and _check_parameter_type(value, value_arg)
            for key, value in value.items()
        )

    return isinstance(value, tpe)
