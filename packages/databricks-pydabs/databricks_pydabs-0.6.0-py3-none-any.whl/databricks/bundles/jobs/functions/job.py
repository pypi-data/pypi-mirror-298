from copy import deepcopy
from dataclasses import dataclass, replace
from typing import Callable, Generic, Optional, ParamSpec, TypeVar

from databricks.bundles.internal._transform import _transient_field
from databricks.bundles.jobs import JobEnvironment
from databricks.bundles.jobs.functions._task_parameters import _TaskParameters
from databricks.bundles.jobs.functions.task import (
    TaskWithOutput,
    _create_task_with_output,
)
from databricks.bundles.jobs.functions.task_parameter import (
    JobParameter,
)
from databricks.bundles.jobs.internal import ast_parser
from databricks.bundles.jobs.internal.inspections import Inspections
from databricks.bundles.jobs.internal.parameters import _serialize_parameter
from databricks.bundles.jobs.models.job import Job, JobParameterDefinition
from databricks.bundles.jobs.models.job_cluster import JobCluster
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.models.tasks.run_job_task import RunJobTask
from databricks.bundles.jobs.transforms import (
    add_default_job_cluster,
    add_default_job_environment,
)
from databricks.bundles.resource import DeferredResource
from databricks.bundles.variables import Variable, resolve_variable

R = TypeVar("R")
P = ParamSpec("P")

_T = TypeVar("_T")


class RunJobTaskWithOutput(TaskWithOutput):
    """
    Task that triggers a job and waits for its completion.
    See :type:`~databricks.bundles.jobs.models.tasks.run_job_task.RunJobTask`.
    """


@dataclass(kw_only=True)
class JobFunction(Generic[P, R], DeferredResource):
    """
    Returns :type:`~RunJobTaskWithOutput` when called within function annotated with
    :func:`@job <databricks.bundles.jobs.job>`.
    """

    base_job: Job
    """
    :meta private: reserved for internal use
    """

    default_job_cluster: Optional[JobCluster]
    """
    :meta private: reserved for internal use
    """

    default_job_environment: Optional[JobEnvironment]
    """
    :meta private: reserved for internal use
    """

    function: Callable[P, R] = _transient_field()  # type:ignore
    """
    :meta private: reserved for internal use
    """

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> TaskWithOutput:
        task_key = Inspections.get_simple_name(self.function)
        base_task = _create_task_with_output(
            task_key=task_key,
            max_retries=None,
            min_retry_interval_millis=None,
            retry_on_timeout=None,
            email_notifications=None,
            webhook_notifications=None,
            notification_settings=None,
            timeout_seconds=None,
            health=None,
        )
        base_task = replace(
            base_task,
            run_job_task=RunJobTask.create(
                job_id=Variable(
                    path=f"resources.jobs.{self.resource_name}.id",
                    type=int,
                )
            ),
        )

        task_parameters = _TaskParameters.parse_call(self.function, args, kwargs)

        return task_parameters.inject(base_task)

    @property
    def value(self) -> Job:
        tasks = self._analyze_tasks(self.function)
        job = deepcopy(self.base_job)
        job = replace(job, tasks=tasks)

        if self.default_job_cluster:
            job = add_default_job_cluster(
                job,
                new_cluster=self.default_job_cluster.new_cluster,
                job_cluster_key=resolve_variable(
                    self.default_job_cluster.job_cluster_key
                ),
            )

        if self.default_job_environment:
            job = add_default_job_environment(
                job,
                spec=resolve_variable(self.default_job_environment.spec) or {},
                environment_key=resolve_variable(
                    self.default_job_environment.environment_key
                ),
            )

        return replace(
            job,
            resource_name=self.resource_name,
        )

    @staticmethod
    def _analyze_tasks(function: Callable) -> list[Task]:
        parameter_signature = Inspections.get_parameter_signatures(function)

        local_vars = {
            name: JobParameter(
                name=name, value_type=sig.tpe, default_value=sig.default_value
            )
            for name, sig in parameter_signature.items()
        }

        scope = ast_parser.Scope(
            closure_vars=Inspections.get_closure_vars(function),
            nonlocals=Inspections.get_closure_nonlocal_vars(function),
            local_vars=local_vars,
            tasks={},
            source_lines=[],
            condition=None,
            file=None,
            start_line_no=None,
        )

        return ast_parser.eval_job_func(function, scope)

    @staticmethod
    def from_job_function(
        function: Callable[P, R],
        *,
        base_job: Job,
        default_job_cluster: Optional[JobCluster] = None,
        default_job_environment: Optional[JobEnvironment] = None,
    ) -> "JobFunction[P, R]":
        """
        :meta private: reserved for internal use
        """

        base_job = replace(
            base_job,
            name=base_job.name or Inspections.get_full_name(function),
            resource_name=base_job.resource_name
            or Inspections.get_resource_name(function),
            description=base_job.description or Inspections.get_docstring(function),
            parameters=base_job.parameters or JobFunction._get_job_parameters(function),
        )

        return JobFunction(
            base_job=base_job,
            resource_name=base_job.resource_name,
            function=function,
            default_job_environment=default_job_environment,
            default_job_cluster=default_job_cluster,
        )

    @staticmethod
    def _get_job_parameters(function: Callable) -> list[JobParameterDefinition]:
        sigs = Inspections.get_parameter_signatures(function)
        parameters = []

        for param_name, sig in sigs.items():
            if not sig.has_default_value:
                raise ValueError(
                    f"Job-level parameter '{param_name}' is missing a default value"
                )

            parameter = JobParameterDefinition(
                name=param_name,
                default=_serialize_parameter(sig.tpe, sig.default_value),
            )

            parameters.append(parameter)

        return parameters
