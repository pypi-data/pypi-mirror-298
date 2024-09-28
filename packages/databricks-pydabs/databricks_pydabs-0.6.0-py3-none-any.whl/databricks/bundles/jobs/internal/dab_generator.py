import json
from dataclasses import replace
from pathlib import Path

from databricks.bundles.compute.models.library import Library
from databricks.bundles.internal._transform_to_json import _transform_to_json_value
from databricks.bundles.jobs import Task
from databricks.bundles.jobs.models.job import Job
from databricks.bundles.variables import Variable, VariableOr, resolve_variable


def _relativize_path(output_file: Path, path_str: str) -> str:
    path = Path(path_str)

    if path.is_absolute():
        return path_str

    if output_file.is_absolute():
        output_file = output_file.relative_to(Path(".").absolute())

    base_dir = output_file.parent

    while base_dir != Path("."):
        path = Path("..") / path
        base_dir = base_dir.parent

    return str(path)


def get_jobs_json(output_file: Path, jobs: dict[str, Job]) -> dict[str, dict]:
    resources = {}

    for name, job in jobs.items():
        if not job.tasks:
            raise ValueError("job.tasks must be set")

        if not isinstance(job.tasks, Variable):
            job = replace(
                job, tasks=[_relativize_task(output_file, task) for task in job.tasks]
            )

        job_resource = _transform_to_json_value(job)

        resources[job.resource_name] = job_resource

    return resources


def generate(output_file: Path, jobs: dict[str, Job]):
    jobs_json = get_jobs_json(output_file, jobs)
    assert jobs_json

    resources_json = json.dumps({"resources": {"jobs": jobs_json}}, indent=2)

    output_file.write_text(resources_json)


def _relativize_task(output_file: Path, task: VariableOr[Task]) -> VariableOr[Task]:
    # we don't need this logic below for PyDABs, so below we just resolve all variables
    # to make pyright happy, instead of carefully trying to preserve them
    # this will always throw an exception if "complex" variable is used

    # the code below also breaks for paths like "s3://" or "dbfs://" which are not relative

    # this will be always true for PyDABs <> CLI integration
    if len(output_file.parts) == 1:
        return task

    # TODO remove code below in 0.6.0

    task = resolve_variable(task)

    # writing to __generated__ changes relative paths, so we have to fix them

    if for_each_task := resolve_variable(task.for_each_task):
        inner_task = resolve_variable(for_each_task.task)

        task = replace(
            task,
            for_each_task=replace(
                for_each_task,
                task=_relativize_task(output_file, inner_task),
            ),
        )
    elif notebook_task := resolve_variable(task.notebook_task):
        notebook_path = _relativize_path(
            output_file=output_file,
            path_str=resolve_variable(notebook_task.notebook_path),
        )

        task = replace(
            task,
            notebook_task=replace(notebook_task, notebook_path=notebook_path),
        )
    elif spark_python_task := resolve_variable(task.spark_python_task):
        python_file_path = _relativize_path(
            output_file=output_file,
            path_str=resolve_variable(spark_python_task.python_file),
        )

        task = replace(
            task,
            spark_python_task=replace(spark_python_task, python_file=python_file_path),
        )
    elif sql_task := resolve_variable(task.sql_task):
        if sql_file_task := resolve_variable(sql_task.file):
            path = _relativize_path(
                output_file=output_file,
                path_str=resolve_variable(sql_file_task.path),
            )

            task = replace(
                task,
                sql_task=replace(sql_task, file=replace(sql_file_task, path=path)),
            )
    elif dbt_task := resolve_variable(task.dbt_task):
        if project_directory := resolve_variable(dbt_task.project_directory):
            project_directory = _relativize_path(
                output_file=output_file,
                path_str=project_directory,
            )

            task = replace(
                task,
                dbt_task=replace(dbt_task, project_directory=project_directory),
            )

    if libraries := resolve_variable(task.libraries):
        task = replace(
            task,
            libraries=[
                _relativize_library_path(output_file, resolve_variable(library))
                for library in libraries
            ],
        )

    return task


def _relativize_library_path(output_file: Path, library: Library) -> Library:
    if whl := resolve_variable(library.whl):
        return replace(
            library,
            whl=_relativize_path(output_file=output_file, path_str=whl),
        )

    if jar := resolve_variable(library.jar):
        return replace(
            library,
            jar=_relativize_path(output_file=output_file, path_str=jar),
        )

    return library
