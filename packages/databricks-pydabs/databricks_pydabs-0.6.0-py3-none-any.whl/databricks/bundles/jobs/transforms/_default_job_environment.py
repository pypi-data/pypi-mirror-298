from dataclasses import dataclass, replace
from typing import Optional

from databricks.bundles.compute.models.environment import Environment, EnvironmentParam
from databricks.bundles.compute.models.library import Library
from databricks.bundles.internal._transform import _transform_variable_or
from databricks.bundles.jobs.models.job import Job
from databricks.bundles.jobs.models.job_cluster import JobCluster
from databricks.bundles.jobs.models.job_environment import JobEnvironment
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.transforms._visitor import _Visitor

__all__ = [
    "add_default_job_environment",
]

from databricks.bundles.variables import (
    Variable,
    VariableOr,
    resolve_variable,
    resolve_variable_or_list,
)


def add_default_job_environment(
    job: Job,
    *,
    spec: VariableOr[EnvironmentParam],
    environment_key: Optional[str] = None,
) -> Job:
    """
    Add default job environment to the job, and every task that doesn't specify
    a cluster. The default job environment will contain all libraries specified in
    tasks. Tasks that don't support clusters (e.g. SQL tasks) are unchanged.

    If no tasks are updated, job cluster is not added to the job, and job is returned unchanged.

    :param job: job to update
    :param spec: default environment for tasks in a job
    :param environment_key: environment_key for added environment or "Default" if None
    :return: updated job
    """

    resolved_spec = _transform_variable_or(Environment, spec)
    resolved_spec = resolve_variable(resolved_spec)
    dependencies = resolve_variable_or_list(resolved_spec.dependencies)

    visitor = _AddDefaultEnvironmentVisitor(
        environment_key=environment_key or JobCluster.DEFAULT_KEY,
        dependencies=dependencies,
        updated=False,
    )

    job = visitor.visit_job(job)

    if visitor.updated:
        job_environment = JobEnvironment(
            environment_key=visitor.environment_key,
            spec=replace(resolved_spec, dependencies=visitor.dependencies),
        )

        environments = resolve_variable(job.environments)

        return replace(job, environments=[*environments, job_environment])
    else:
        return job


@dataclass(kw_only=True)
class _AddDefaultEnvironmentVisitor(_Visitor):
    environment_key: VariableOr[str]
    dependencies: list[str]
    updated: bool

    def visit_compute_task(self, task: Task) -> Task:
        if (
            task.new_cluster
            or task.job_cluster_key
            or task.environment_key
            or task.existing_cluster_id
        ) and task.environment_key != self.environment_key:
            return task

        if task.spark_submit_task:
            raise ValueError(
                "SparkSubmitTask can't use serverless clusters and should specify new_cluster"
            )

        libraries = resolve_variable(task.libraries)

        if task.notebook_task and libraries:
            raise ValueError(
                "Notebook tasks can't specify libraries when running on serverless clusters, "
                "specify libraries in the notebook instead"
            )

        if task.notebook_task:
            # notebook tasks don't to specify environment_key
            return task

        self.updated = True

        for library in libraries:
            dependency = _get_library_dependency(resolve_variable(library))

            if dependency not in self.dependencies:
                self.dependencies.append(dependency)

        return replace(
            task,
            environment_key=self.environment_key,
            libraries=[],
        )


def _get_library_dependency(library: Library) -> str:
    if whl := library.whl:
        return _stringify(whl)
    elif egg := library.egg:
        return _stringify(egg)
    elif library.requirements:
        return f"-r {_stringify(library.requirements)}"
    elif pypi := resolve_variable(library.pypi):
        if pypi.repo:
            repo = _stringify(pypi.repo)
            package = _stringify(pypi.package)

            return f"--extra-index-url={repo} {package}"
        else:
            return _stringify(pypi.package)
    elif library.cran:
        raise ValueError("CRAN libraries are not supported for serverless clusters")
    elif library.jar:
        raise ValueError("JAR libraries are not supported for serverless clusters")
    elif library.maven:
        raise ValueError("Maven libraries are not supported for serverless clusters")
    else:
        raise ValueError(f"Unknown library type: {library}")


def _stringify(value: VariableOr[str]) -> str:
    if isinstance(value, Variable):
        return value.value
    else:
        return value
