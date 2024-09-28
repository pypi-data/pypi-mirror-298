import argparse
import importlib


def _create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_func")

    return parser


def main():
    from databricks.bundles.jobs.internal import executor

    parser = _create_argument_parser()
    parsed, remaining_args = parser.parse_known_args()

    module_name, task_name = parsed.task_func.split(":")

    module = importlib.import_module(module_name)
    task = getattr(module, task_name)

    executor.run_python_task_from_wheel(task, remaining_args)
