import inspect
import logging
import traceback
from dataclasses import dataclass
from io import StringIO
from typing import Any, Callable, ClassVar, Optional

from databricks.bundles.internal._diagnostics import (
    Diagnostic,
    Diagnostics,
    Location,
    Severity,
)
from databricks.bundles.jobs import Job, JobSyntaxError
from databricks.bundles.resource import (
    DeferredResource,
    Resource,
    ResourceGenerator,
    ResourceMutator,
)


@dataclass(frozen=True, eq=True, kw_only=True)
class _ResourceType:
    """
    Resource types supported by _Loader. Values should correspond to the keys in the resources dict.
    """

    plural_name: str

    JOBS: ClassVar["_ResourceType"]


_ResourceType.JOBS = _ResourceType(plural_name="jobs")


class _Loader:
    """
    Loader reads resources, resource generators and mutators from Python modules and YAML files.

    Mutators and resource generators are only loaded, and not applied.
    """

    def __init__(self):
        self._jobs = dict[str, Job]()
        self._mutators = list[ResourceMutator]()
        self._resource_generators = list[ResourceGenerator]()
        self._locations = dict[tuple[_ResourceType, str], Location]()

    def get_location(self, obj: Resource | ResourceMutator) -> Optional[Location]:
        if isinstance(obj, ResourceMutator):
            return Location.from_callable(obj.function)

        if isinstance(obj, ResourceGenerator):
            return Location.from_callable(obj.function)

        if isinstance(obj, DeferredResource):
            return self.get_location(obj.value)

        assert isinstance(obj, Job)
        assert obj.resource_name

        resource_type = _get_resource_type(obj)

        return self._locations.get((resource_type, obj.resource_name))

    @property
    def jobs(self) -> dict[str, Job]:
        return self._jobs

    @property
    def mutators(self) -> list[ResourceMutator]:
        return self._mutators

    @property
    def resource_generators(self) -> list[ResourceGenerator]:
        return self._resource_generators

    def register_module(self, module: Any, *, override: bool) -> Diagnostics:
        diagnostics = Diagnostics()

        for _, resource in _getmembers_ordered(module, _is_resource):
            logging.debug("Discovered job %s", resource.resource_name)

            diagnostics = diagnostics.extend(
                self.register_resource(resource, override=override)
            )

        for _, mutator in _getmembers_ordered(module, _is_mutator):
            if mutator in self._mutators:
                continue

            logging.debug("Discovered resource mutator %s", mutator.function.__name__)

            self._mutators.append(mutator)

        for _, generator in _getmembers_ordered(module, _is_resource_generator):
            if generator in self._resource_generators:
                continue

            logging.debug(
                "Discovered resource generator %s", generator.function.__name__
            )

            self._resource_generators.append(generator)

        return diagnostics

    def register_bundle_config(self, bundle: dict) -> Diagnostics:
        diagnostics = Diagnostics()
        jobs_dict = bundle.get("resources", {}).get("jobs", {})

        for resource_name, job_dict in jobs_dict.items():
            try:
                job = Job.create(resource_name=resource_name, **job_dict)
            except Exception as exc:
                return diagnostics.extend(
                    Diagnostics.from_exception(
                        exc=exc,
                        summary="Error while loading job",
                        path=f"resources.jobs.{resource_name}",
                    )
                )

            diagnostics = diagnostics.extend(self.register_job(job, override=False))

        return diagnostics

    def register_resource(
        self, resource: Resource, *, override: bool, location: Optional[Location] = None
    ) -> Diagnostics:
        match resource:
            case Job() as job:
                return self.register_job(job, override=override, location=location)

            case DeferredResource() as deferred:
                try:
                    try:
                        deferred.value
                    except JobSyntaxError as exc:
                        return _translate_job_syntax_error(exc)
                    except Exception as exc:
                        return Diagnostics.from_exception(
                            exc=exc,
                            summary=f"Error while loading '{deferred.resource_name}'",
                            location=_find_resource_location(deferred),
                        )

                    location = _find_resource_location(deferred)
                    diag = self.register_resource(
                        deferred.value, override=override, location=location
                    )

                    return diag.with_location_if_absent(location)

                except Exception as exc:
                    return Diagnostics.from_exception(
                        exc=exc,
                        summary=f"Error while loading '{deferred.resource_name}'",
                        location=_find_resource_location(deferred),
                    )

        raise ValueError(f"Unsupported resource type: {type(resource)}")

    def _register_location(self, resource: Resource, location: Location):
        assert resource.resource_name

        resource_type = _get_resource_type(resource)

        self._locations[(resource_type, resource.resource_name)] = location

    def register_job(
        self, job: Job, *, override: bool, location: Optional[Location] = None
    ) -> Diagnostics:
        """
        :param job: job to register
        :param override: if true, allow overwriting an existing job with the same resource_name
        :param location: optional location of where the job was last defined or updated
        """

        assert isinstance(job, Job)

        diagnostics = Diagnostics()

        if not job.resource_name:
            return diagnostics.extend(
                Diagnostics.create_error(
                    msg="resource_name is required for a job",
                    location=None,
                )
            )

        existing_job = self._jobs.get(job.resource_name)

        if existing_job and not override:
            return diagnostics.extend(
                Diagnostics.create_error(
                    msg=f"Two jobs have the same resource_name '{job.resource_name}'",
                    location=None,
                )
            )

        # NB: not very reliable because job can be simply mutated
        if existing_job is not job and location:
            self._register_location(job, location)

        self._jobs[job.resource_name] = job

        return diagnostics


def _find_resource_location(resource: Resource) -> Optional[Location]:
    if function := getattr(resource, "function", None):
        return Location.from_callable(function)

    return None


def _get_resource_type(resource: Resource) -> _ResourceType:
    if isinstance(resource, DeferredResource):
        return _get_resource_type(resource.value)

    assert isinstance(resource, Job)

    return _ResourceType.JOBS


def _translate_job_syntax_error(exc: JobSyntaxError) -> Diagnostics:
    detail = StringIO()
    detail.writelines(traceback.format_exception_only(exc))

    location = (
        Location(
            file=exc.filename,
            line=exc.lineno or 1,
            column=exc.offset or 1,
        )
        if exc.filename
        else None
    )

    return Diagnostics(
        items=[
            Diagnostic(
                severity=Severity.ERROR,
                summary=exc.msg,
                detail=detail.getvalue(),
                location=location,
            )
        ]
    )


def _is_resource(obj):
    return isinstance(obj, Resource)


def _is_resource_generator(obj):
    return isinstance(obj, ResourceGenerator)


def _is_mutator(obj):
    return isinstance(obj, ResourceMutator)


def _getmembers_ordered(obj, predicate: Callable[[Any], bool]):
    """Get members in the order they are defined in the module."""

    members = inspect.getmembers(obj, predicate)
    priority = {key: idx for idx, key in enumerate(vars(obj).keys())}

    members.sort(key=lambda kv: priority.get(kv[0], 0))

    return members
