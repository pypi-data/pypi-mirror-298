from dataclasses import dataclass, replace
from typing import TYPE_CHECKING, Callable, TypeVar

from databricks.bundles.jobs.functions.task_parameter import (
    ConstantParameter,
    ForEachInputTaskParameter,
    JobParameter,
    TaskParameter,
    TaskReferenceParameter,
    VariableParameter,
)
from databricks.bundles.jobs.internal.inspections import Inspections
from databricks.bundles.jobs.internal.parameters import _serialize_parameter
from databricks.bundles.jobs.models.task import Task, TaskDependency
from databricks.bundles.variables import resolve_variable

if TYPE_CHECKING:
    from typing_extensions import Self

_TaskT = TypeVar("_TaskT", bound=Task)


@dataclass
class _TaskParameters:
    parameters: dict[str, str]
    task_dependencies: list[str]

    @classmethod
    def parse_call(cls, function: Callable, args: tuple, kwargs: dict) -> "Self":
        if function:
            named_parameters = Inspections.to_named_parameters(function, args, kwargs)
        else:
            if len(args) != 0:
                raise ValueError("Only keyword arguments are supported")

            named_parameters = kwargs

        parameters = {}
        depends_on = set[str]()
        parameter_types = Inspections.get_parameters(function)

        for key, value in named_parameters.items():
            if isinstance(value, ConstantParameter):
                value = value.value

            parameter_type = parameter_types.get(key)
            assert parameter_type, f"can't find parameter type for '{key}'"

            if isinstance(value, TaskParameter):
                for depends_on_key in cls._get_depends_on(value):
                    depends_on.add(depends_on_key)

                parameters[key] = cls._serialize_task_parameter(value, parameter_type)
            else:
                # using parameter_type to give a better type hint in case parameterized types are used
                parameters[key] = _serialize_parameter(parameter_type, value)

        return cls(
            parameters=parameters,
            task_dependencies=sorted(set(depends_on)),
        )

    @classmethod
    def _serialize_task_parameter(
        cls, task_parameter: TaskParameter, parameter_type: type
    ) -> str:
        match task_parameter:
            case TaskReferenceParameter():
                return task_parameter.serialize()
            case JobParameter():
                return task_parameter.serialize()
            case ForEachInputTaskParameter():
                return task_parameter.serialize()
            case VariableParameter():
                return task_parameter.serialize()
            case ConstantParameter():
                # using parameter_type to give a better type hint in case parameterized types are used
                return _serialize_parameter(parameter_type, task_parameter.value)

        raise ValueError(f"Unsupported task parameter type: {task_parameter}")

    @classmethod
    def _get_depends_on(cls, task_parameter: TaskParameter) -> list[str]:
        match task_parameter:
            case TaskReferenceParameter():
                return [task_parameter.task_key]
            case ForEachInputTaskParameter():
                return []
            case JobParameter():
                return []
            case ConstantParameter():
                return []
            case VariableParameter():
                return []

        raise ValueError(f"Unsupported task parameter type: {task_parameter}")

    def inject(self, task: _TaskT) -> _TaskT:
        parameter_list = [
            f"--{name}={parameter}" for name, parameter in self.parameters.items()
        ]

        # copy because we are going to mutate it
        depends_on = [*resolve_variable(task.depends_on)]

        for task_key in self.task_dependencies:
            task_dependency = TaskDependency(task_key)

            if task_dependency not in depends_on:
                depends_on.append(task_dependency)

        task = replace(
            task,
            depends_on=depends_on,
        )

        # TODO spark_submit_task

        if notebook_task := resolve_variable(task.notebook_task):
            parameters = resolve_variable(notebook_task.base_parameters)

            return replace(
                task,
                notebook_task=replace(
                    notebook_task,
                    base_parameters={**parameters, **self.parameters},
                ),
            )
        elif spark_jar_task := resolve_variable(task.spark_jar_task):
            parameters = resolve_variable(spark_jar_task.parameters)

            return replace(
                task,
                spark_jar_task=replace(
                    spark_jar_task,
                    parameters=[*parameters, *parameter_list],
                ),
            )
        elif spark_python_task := resolve_variable(task.spark_python_task):
            parameters = resolve_variable(spark_python_task.parameters)

            return replace(
                task,
                spark_python_task=replace(
                    spark_python_task,
                    parameters=[*parameters, *parameter_list],
                ),
            )

        elif sql_task := resolve_variable(task.sql_task):
            parameters = resolve_variable(sql_task.parameters)

            # note: SQL alerts don't support parameters

            return replace(
                task,
                sql_task=replace(
                    sql_task,
                    parameters={**parameters, **self.parameters},
                ),
            )
        elif python_wheel_task := resolve_variable(task.python_wheel_task):
            parameters = resolve_variable(python_wheel_task.parameters)

            return replace(
                task,
                python_wheel_task=replace(
                    python_wheel_task,
                    parameters=[*parameters, *parameter_list],
                ),
            )
        elif run_job_task := resolve_variable(task.run_job_task):
            job_parameters = resolve_variable(run_job_task.job_parameters)

            return replace(
                task,
                run_job_task=replace(
                    run_job_task, job_parameters={**job_parameters, **self.parameters}
                ),
            )
        elif (
            task.condition_task
            or task.dbt_task
            or task.pipeline_task
            or task.for_each_task
        ):
            # no parameters
            return task
        else:
            raise ValueError(f"Unsupported task type: {task}")
