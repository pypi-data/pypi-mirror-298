import abc
from dataclasses import dataclass
from typing import Any, Callable, Generic, Iterator, Optional, Type, TypeVar, overload

from databricks.bundles.internal._transform import _transient_field

T = TypeVar("T")

__all__ = [
    "Resource",
    "ResourceGenerator",
    "ResourceMutator",
    "resource_generator",
]


@dataclass
class Resource:
    """
    Common type for all resources that can be used in a bundle.
    """

    resource_name: Optional[str] = _transient_field()  # type:ignore
    """
    Unique identifier for the resource. If not provided, resources declared using decorators
    are assigned an unique identifier based on the function name.
    
    If a resource name is changed, the resource is going to be destroyed and recreated during the
    next deployment.
    """


@dataclass
class DeferredResource(Resource):
    @property
    @abc.abstractmethod
    def value(self) -> Resource:
        ...


@dataclass(frozen=True)
class ResourceGenerator:
    """
    See :attr:`@resource_generator <databricks.bundles.resource.resource_generator>` to create a new
    resource generator.
    """

    function: Callable[[], Iterator[Resource]]
    """
    Underling function that was decorated. Can be accessed for unit-testing.
    """


@dataclass(frozen=True)
class ResourceMutator(Generic[T]):
    """
    Mutators defined within a single Python module are applied in the order they are defined.
    The relative order of mutators defined in different modules is not guaranteed.

    See :meth:`databricks.bundles.jobs.job_mutator`.
    """

    resource_type: Type[T]
    """
    Resource type that this mutator applies to.
    """

    function: Callable[[T], T]
    """
    Underling function that was decorated. Can be accessed for unit-testing.
    """


@overload
def resource_generator(function: Callable[[], Iterator[Resource]]) -> ResourceGenerator:
    """
    Decorator that transform function into a resource generator.

    Resource generators can dynamically create resources during the bundle deployment.
    Resource generators can access bundle variables

    .. code-block:: python

        from databricks.bundles.jobs import job
        from databricks.bundles.resource import resource_generator

        def create_job(country: str):
            # each generated job must have unique resource name
            @job(resource_name=f"send_report_{country}")
            def my_job():
                send_report(country=country)

        @resource_generator
        def my_resource_generator():
            for country in ["NL", "US"]:
                yield create_job(country)


    See `Generate jobs and tasks dynamically <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/resource-generators.html>`_.

    Resource generators can be completed with data classes for creating more complex resources, for example,
    jobs with dynamic number of tasks. See
    `Create jobs using dataclasses <https://docs.databricks.com/en/dev-tools/bundles/python/how-to/job-dataclass.html>`_.
    """
    ...


@overload
def resource_generator() -> (
    Callable[[Callable[[], Iterator[Resource]]], ResourceGenerator]
):
    ...


def resource_generator(*args: Any, **kwargs: Any) -> Any:
    # using `@resource_generator` is equivalent to `@resource_generator()`
    if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
        # assuming that args[0] is Callable[[], Iterator[Resource]]
        return resource_generator()(args[0])  # type:ignore

    if len(args) != 0:
        raise ValueError("Only keyword args are supported")

    def wrapper(function: Callable[[], Iterator[Resource]]) -> ResourceGenerator:
        return ResourceGenerator(function)

    return wrapper
