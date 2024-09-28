from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, Literal, Optional, TypedDict

from databricks.bundles.internal._transform import _transform
from databricks.bundles.jobs.models.pause_status import PauseStatus, PauseStatusParam
from databricks.bundles.variables import VariableOr, VariableOrList, VariableOrOptional

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = [
    "Condition",
    "ConditionParam",
    "Continuous",
    "ContinuousParam",
    "FileArrivalTriggerConfiguration",
    "FileArrivalTriggerConfigurationParam",
    "PeriodicTriggerConfigurationTimeUnit",
    "PeriodicTriggerConfigurationTimeUnitParam",
    "PeriodicTriggerConfiguration",
    "PeriodicTriggerConfigurationParam",
    "TableUpdateTriggerConfiguration",
    "TableUpdateTriggerConfigurationParam",
    "TriggerSettings",
    "TriggerSettingsParam",
]


class Condition(Enum):
    ANY_UPDATED = "ANY_UPDATED"
    ALL_UPDATED = "ALL_UPDATED"


ConditionParam = Literal["ANY_UPDATED", "ALL_UPDATED"] | Condition


@dataclass(kw_only=True)
class Continuous:
    """"""

    pause_status: VariableOrOptional[PauseStatus] = None
    """
    Indicate whether the continuous execution of the job is paused or not. Defaults to UNPAUSED.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        pause_status: VariableOrOptional[PauseStatusParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class ContinuousDict(TypedDict, total=False):
    """"""

    pause_status: VariableOrOptional[PauseStatusParam]
    """
    Indicate whether the continuous execution of the job is paused or not. Defaults to UNPAUSED.
    """


ContinuousParam = ContinuousDict | Continuous


@dataclass(kw_only=True)
class FileArrivalTriggerConfiguration:
    """"""

    url: VariableOr[str]
    """
    URL to be monitored for file arrivals. The path must point to the root or a subpath of the external location.
    """

    min_time_between_triggers_seconds: VariableOrOptional[int] = None
    """
    If set, the trigger starts a run only after the specified amount of time passed since
    the last time the trigger fired. The minimum allowed value is 60 seconds
    """

    wait_after_last_change_seconds: VariableOrOptional[int] = None
    """
    If set, the trigger starts a run only after no file activity has occurred for the specified amount of time.
    This makes it possible to wait for a batch of incoming files to arrive before triggering a run. The
    minimum allowed value is 60 seconds.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        url: VariableOr[str],
        min_time_between_triggers_seconds: VariableOrOptional[int] = None,
        wait_after_last_change_seconds: VariableOrOptional[int] = None,
    ) -> "Self":
        return _transform(cls, locals())


class FileArrivalTriggerConfigurationDict(TypedDict, total=False):
    """"""

    url: VariableOr[str]
    """
    URL to be monitored for file arrivals. The path must point to the root or a subpath of the external location.
    """

    min_time_between_triggers_seconds: VariableOrOptional[int]
    """
    If set, the trigger starts a run only after the specified amount of time passed since
    the last time the trigger fired. The minimum allowed value is 60 seconds
    """

    wait_after_last_change_seconds: VariableOrOptional[int]
    """
    If set, the trigger starts a run only after no file activity has occurred for the specified amount of time.
    This makes it possible to wait for a batch of incoming files to arrive before triggering a run. The
    minimum allowed value is 60 seconds.
    """


FileArrivalTriggerConfigurationParam = (
    FileArrivalTriggerConfigurationDict | FileArrivalTriggerConfiguration
)


class PeriodicTriggerConfigurationTimeUnit(Enum):
    HOURS = "HOURS"
    DAYS = "DAYS"
    WEEKS = "WEEKS"


PeriodicTriggerConfigurationTimeUnitParam = (
    Literal["HOURS", "DAYS", "WEEKS"] | PeriodicTriggerConfigurationTimeUnit
)


@dataclass(kw_only=True)
class PeriodicTriggerConfiguration:
    """"""

    interval: VariableOr[int]
    """
    The interval at which the trigger should run.
    """

    unit: VariableOr[PeriodicTriggerConfigurationTimeUnit]
    """
    The unit of time for the interval.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        interval: VariableOr[int],
        unit: VariableOr[PeriodicTriggerConfigurationTimeUnitParam],
    ) -> "Self":
        return _transform(cls, locals())


class PeriodicTriggerConfigurationDict(TypedDict, total=False):
    """"""

    interval: VariableOr[int]
    """
    The interval at which the trigger should run.
    """

    unit: VariableOr[PeriodicTriggerConfigurationTimeUnitParam]
    """
    The unit of time for the interval.
    """


PeriodicTriggerConfigurationParam = (
    PeriodicTriggerConfigurationDict | PeriodicTriggerConfiguration
)


@dataclass(kw_only=True)
class TableUpdateTriggerConfiguration:
    """"""

    condition: VariableOrOptional[Condition] = None
    """
    The table(s) condition based on which to trigger a job run.
    """

    min_time_between_triggers_seconds: VariableOrOptional[int] = None
    """
    If set, the trigger starts a run only after the specified amount of time has passed since
    the last time the trigger fired. The minimum allowed value is 60 seconds.
    """

    table_names: VariableOrList[str] = field(default_factory=list)
    """
    A list of Delta tables to monitor for changes. The table name must be in the format `catalog_name.schema_name.table_name`.
    """

    wait_after_last_change_seconds: VariableOrOptional[int] = None
    """
    If set, the trigger starts a run only after no table updates have occurred for the specified time
    and can be used to wait for a series of table updates before triggering a run. The
    minimum allowed value is 60 seconds.
    """

    @classmethod
    def create(
        cls,
        /,
        *,
        condition: VariableOrOptional[ConditionParam] = None,
        min_time_between_triggers_seconds: VariableOrOptional[int] = None,
        table_names: Optional[VariableOrList[str]] = None,
        wait_after_last_change_seconds: VariableOrOptional[int] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TableUpdateTriggerConfigurationDict(TypedDict, total=False):
    """"""

    condition: VariableOrOptional[ConditionParam]
    """
    The table(s) condition based on which to trigger a job run.
    """

    min_time_between_triggers_seconds: VariableOrOptional[int]
    """
    If set, the trigger starts a run only after the specified amount of time has passed since
    the last time the trigger fired. The minimum allowed value is 60 seconds.
    """

    table_names: VariableOrList[str]
    """
    A list of Delta tables to monitor for changes. The table name must be in the format `catalog_name.schema_name.table_name`.
    """

    wait_after_last_change_seconds: VariableOrOptional[int]
    """
    If set, the trigger starts a run only after no table updates have occurred for the specified time
    and can be used to wait for a series of table updates before triggering a run. The
    minimum allowed value is 60 seconds.
    """


TableUpdateTriggerConfigurationParam = (
    TableUpdateTriggerConfigurationDict | TableUpdateTriggerConfiguration
)


@dataclass(kw_only=True)
class TriggerSettings:
    """"""

    file_arrival: VariableOrOptional[FileArrivalTriggerConfiguration] = None
    """
    File arrival trigger settings.
    """

    pause_status: VariableOrOptional[PauseStatus] = None
    """
    Whether this trigger is paused or not.
    """

    periodic: VariableOrOptional[PeriodicTriggerConfiguration] = None
    """
    Periodic trigger settings.
    """

    table_update: VariableOrOptional[TableUpdateTriggerConfiguration] = None

    def __post_init__(self):
        union_fields = [
            self.file_arrival,
            self.periodic,
            self.table_update,
        ]

        if sum(f is not None for f in union_fields) != 1:
            raise ValueError(
                "TriggerSettings must specify exactly one of 'file_arrival', 'periodic', 'table_update'"
            )

    @classmethod
    def create(
        cls,
        /,
        *,
        file_arrival: VariableOrOptional[FileArrivalTriggerConfigurationParam] = None,
        pause_status: VariableOrOptional[PauseStatusParam] = None,
        periodic: VariableOrOptional[PeriodicTriggerConfigurationParam] = None,
        table_update: VariableOrOptional[TableUpdateTriggerConfigurationParam] = None,
    ) -> "Self":
        return _transform(cls, locals())


class TriggerSettingsDict(TypedDict, total=False):
    """"""

    file_arrival: VariableOrOptional[FileArrivalTriggerConfigurationParam]
    """
    File arrival trigger settings.
    """

    pause_status: VariableOrOptional[PauseStatusParam]
    """
    Whether this trigger is paused or not.
    """

    periodic: VariableOrOptional[PeriodicTriggerConfigurationParam]
    """
    Periodic trigger settings.
    """

    table_update: VariableOrOptional[TableUpdateTriggerConfigurationParam]


TriggerSettingsParam = TriggerSettingsDict | TriggerSettings
