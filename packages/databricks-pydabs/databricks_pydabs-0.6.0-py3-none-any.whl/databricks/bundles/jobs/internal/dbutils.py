from typing import Any, Optional


class Dbutils:
    @classmethod
    def get_notebook_path(cls):
        java_dbutils = _get_java_dbutils()

        return _unwrap_option(java_dbutils.notebook().getContext().notebookPath())

    @classmethod
    def get_api_token(cls) -> Optional[str]:
        java_dbutils = _get_java_dbutils()

        return _unwrap_option(java_dbutils.notebook().getContext().apiToken())

    @classmethod
    def get_api_url(cls) -> Optional[str]:
        java_dbutils = _get_java_dbutils()

        return _unwrap_option(java_dbutils.notebook().getContext().apiUrl())

    @classmethod
    def exit(cls, output: Any):
        # this line is only called from Databricks clusters
        from databricks.sdk.runtime import dbutils  # type:ignore

        # ignore problems with type stubs
        dbutils.notebook.exit(output)  # type: ignore

    @classmethod
    def get_task_func(cls) -> Optional[str]:
        return cls.get_parameter("task_func")

    @classmethod
    def get_parameter(cls, name: str) -> Optional[str]:
        # this line is only called from Databricks clusters
        from databricks.sdk.runtime import dbutils  # type:ignore

        try:
            return dbutils.widgets.get(name)
        except:  # noqa
            return None

    @classmethod
    def set_task_value(cls, key: str, value: Any):
        # this line is only called from Databricks clusters
        from databricks.sdk.runtime import dbutils  # type:ignore

        dbutils.jobs.taskValues.set(key, value)  # type: ignore


def _get_java_dbutils():
    # this line is only called from Databricks clusters
    from databricks.sdk.runtime import dbutils  # type:ignore

    return dbutils.notebook.entry_point.getDbutils()  # type: ignore


def _unwrap_option(option) -> Optional[str]:
    if option.isDefined():
        return option.get()
    else:
        return None
