from dataclasses import replace

from databricks.bundles.jobs.models.job import Job
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.variables import resolve_variable


class _Visitor:
    def visit_compute_task(self, task: Task) -> Task:
        return task

    def visit_job(self, job: Job) -> Job:
        tasks = resolve_variable(job.tasks)

        return replace(
            job,
            tasks=[self.visit_task(resolve_variable(task)) for task in tasks],
        )

    def visit_task(self, task: Task) -> Task:
        if task.sql_task:
            return task
        elif notebook_task := resolve_variable(task.notebook_task):
            if notebook_task.warehouse_id:
                return task
            else:
                return self.visit_compute_task(task)
        elif for_each_task := resolve_variable(task.for_each_task):
            return replace(
                task,
                for_each_task=replace(
                    for_each_task,
                    task=self.visit_task(resolve_variable(for_each_task.task)),
                ),
            )
        elif task.python_wheel_task:
            return self.visit_compute_task(task)
        elif task.pipeline_task:
            # pipeline tasks can't use job clusters
            return task
        elif task.run_job_task:
            return task
        elif task.condition_task:
            return task
        elif task.dbt_task:
            return self.visit_compute_task(task)
        elif task.spark_jar_task:
            return self.visit_compute_task(task)
        elif task.spark_submit_task:
            return self.visit_compute_task(task)
        elif task.spark_python_task:
            return self.visit_compute_task(task)

        raise ValueError(f"Unknown task type: {task}")
