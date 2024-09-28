from databricks.bundles.internal._transform_to_json import _transform_to_json_value
from databricks.bundles.jobs.functions._signature import Signature
from databricks.bundles.jobs.functions.compute import ComputeTaskFunction
from databricks.bundles.jobs.internal.dbutils import Dbutils
from databricks.bundles.jobs.internal.parameters import _deserialize_parameter


def run_python_task_from_wheel(task: ComputeTaskFunction, argv: list[str]):
    params = _parse_argv(task, argv)

    run_python_task(task, params)


def run_python_task(task: ComputeTaskFunction, params: dict[str, str]):
    kwargs = {}
    signature = Signature.from_function(task.function)

    for param_name, value_type in signature.parameters.items():
        value = params.get(param_name)

        if value is not None:
            kwargs[param_name] = _deserialize_parameter(value, value_type)

    output = task.function.__call__(**kwargs)  # type:ignore

    if "return_value" in signature.return_type:
        output = _transform_to_json_value(output)

        Dbutils.set_task_value("return_value", output)


def _parse_argv(task: ComputeTaskFunction, argv: list[str]) -> dict[str, str]:
    import argparse

    parser = argparse.ArgumentParser()
    signature = Signature.from_function(task.function)

    for param_name, _ in signature.parameters.items():
        parser.add_argument(f"--{param_name}")

    args, _ = parser.parse_known_args(argv)

    return vars(args)
