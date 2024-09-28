from dataclasses import dataclass, replace
from typing import Optional

from databricks.bundles.compute.models.cluster_spec import ClusterSpec, ClusterSpecParam
from databricks.bundles.internal._transform import _transform_variable_or
from databricks.bundles.jobs.models.job import Job
from databricks.bundles.jobs.models.job_cluster import JobCluster
from databricks.bundles.jobs.models.task import Task
from databricks.bundles.jobs.transforms._visitor import _Visitor

__all__ = [
    "add_default_job_cluster",
]

from databricks.bundles.variables import (
    VariableOr,
    resolve_variable,
)


def add_default_job_cluster(
    job: Job,
    *,
    new_cluster: VariableOr[ClusterSpecParam],
    job_cluster_key: Optional[str] = None,
) -> Job:
    """
    Add default job cluster to the job, and every task that doesn't specify a cluster.
    Tasks that don't support clusters (e.g. SQL tasks) are unchanged.

    If no tasks are updated, job cluster is not added to the job, and job is returned unchanged.

    :param job: job to update
    :param new_cluster: cluster spec for default cluster
    :param job_cluster_key: job_cluster_key for added job cluster or "Default" if None
    :return: updated job
    """

    resolved_new_cluster = _transform_variable_or(ClusterSpec, new_cluster)

    visitor = _AddDefaultJobClusterVisitor(
        job_cluster_key=job_cluster_key or JobCluster.DEFAULT_KEY,
        updated=False,
    )

    updated_job = visitor.visit_job(job)

    if visitor.updated:
        job_cluster = JobCluster(
            job_cluster_key=job_cluster_key or JobCluster.DEFAULT_KEY,
            new_cluster=resolved_new_cluster,
        )
        job_clusters = resolve_variable(updated_job.job_clusters)

        return replace(updated_job, job_clusters=[*job_clusters, job_cluster])
    else:
        return job


@dataclass(kw_only=True)
class _AddDefaultJobClusterVisitor(_Visitor):
    job_cluster_key: str
    updated: bool

    def visit_compute_task(self, task: Task) -> Task:
        if (
            task.new_cluster
            or task.job_cluster_key
            or task.environment_key
            or task.existing_cluster_id
        ) and task.job_cluster_key != self.job_cluster_key:
            return task

        if task.spark_submit_task:
            raise ValueError(
                "SparkSubmitTask can't use job clusters and should specify new_cluster"
            )

        self.updated = True

        return replace(task, job_cluster_key=self.job_cluster_key)
