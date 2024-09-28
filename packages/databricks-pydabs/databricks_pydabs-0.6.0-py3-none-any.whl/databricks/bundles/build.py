import argparse
import importlib.metadata
import importlib.util
import json
import logging
import pkgutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, TextIO

from databricks.bundles.internal._diagnostics import (
    Diagnostics,
    Location,
    Severity,
)
from databricks.bundles.internal._loader import _Loader
from databricks.bundles.jobs.internal import dab_generator
from databricks.bundles.jobs.models.job import Job
from databricks.bundles.variables import VariableContext


def _run_load(
    loader: _Loader,
    module_names: list[str],
    *,
    override: bool,
) -> Diagnostics:
    diagnostics = Diagnostics()

    for module_name in module_names:
        try:
            logging.debug(f"Loading '{module_name}'")

            module = importlib.import_module(module_name)

            diagnostics = diagnostics.extend(
                loader.register_module(module, override=override)
            )
        except Exception as exc:
            return diagnostics.extend(
                Diagnostics.from_exception(
                    exc=exc,
                    # TODO there must be a way to get location of the module without loading it
                    # through importlib.util.find_spec
                    location=None,
                    summary=f"Failed to load module '{module_name}'",
                )
            )

    return diagnostics


def _run_init(loader: _Loader) -> Diagnostics:
    diagnostics = Diagnostics()

    for resource_generator in loader.resource_generators:
        try:
            for resource in resource_generator.function():
                diagnostics = diagnostics.extend(
                    loader.register_resource(resource, override=False)
                )

        except Exception as exc:
            return diagnostics.extend(
                Diagnostics.from_exception(
                    exc=exc,
                    location=Location.from_callable(resource_generator.function),
                    summary=f"Failed to apply resource generator '{resource_generator.function.__name__}'",
                )
            )

    if diagnostics.has_error():
        return diagnostics

    for resource_name, job in loader.jobs.items():
        last_location = None

        for mutator in loader.mutators:
            try:
                if mutator.resource_type == Job:
                    new_job = mutator.function(job)

                    # NB: not very reliable, because job can be simply mutated
                    if new_job is not job:
                        job = new_job
                        last_location = loader.get_location(mutator)

            except Exception as exc:
                return diagnostics.extend(
                    Diagnostics.from_exception(
                        exc=exc,
                        location=Location.from_callable(mutator.function),
                        summary=f"Failed to apply job mutator '{mutator.function.__name__}' to job '{job.resource_name}'",
                    )
                )

        diagnostics = diagnostics.extend(
            loader.register_job(job, override=True, location=last_location)
        )

    return diagnostics


def _load_bundle(
    bundle: dict,
    module_names: list[str],
    only_load: bool,
) -> tuple[_Loader, Diagnostics]:
    loader = _Loader()

    diagnostics = Diagnostics()
    diagnostics = diagnostics.extend(loader.register_bundle_config(bundle))

    if diagnostics.has_error():
        return loader, diagnostics

    if only_load:
        # On 'load' phase, we expect a 'clean' state and no overrides are needed
        diagnostics = diagnostics.extend(
            _run_load(loader, module_names, override=False)
        )
    else:
        # On 'init' phase, we 'bundle' contains resources from 'load' phase
        #
        # Instead of reading them as-is, we override them with resources loaded
        # in Python code, that should be equivalent. Additionally, it gives
        # us types that are erased with JSON serialization.
        #
        # For instance, all ComputeTask are serialized as Task, and instanceof checks
        # aren't going to work anymore in job mutators.

        load_diagnostics = _run_load(loader, module_names, override=True)

        # we ignore warnings in _run_load because we have already reported them at 'load' stage
        if load_diagnostics.has_error():
            return loader, load_diagnostics

        variables = {k: v.get("value") for k, v in bundle.get("variables", {}).items()}

        with VariableContext.push(variables):
            diagnostics = diagnostics.extend(_run_init(loader))

    return loader, diagnostics


def _write_locations(f: TextIO, loader: _Loader):
    for resource_name, job in loader.jobs.items():
        if location := loader.get_location(job):
            path = f"resources.jobs.{resource_name}"
            json.dump({"path": path, **location.to_json()}, f)
            f.write("\n")


def _update_bundle(bundle: dict, loader: _Loader):
    jobs_dict = dab_generator.get_jobs_json(
        # this is only used to relativize paths
        output_file=Path("__generated__.yml"),
        jobs=loader.jobs,
    )

    bundle["resources"] = bundle.get("resources", {})
    bundle["resources"]["jobs"] = jobs_dict


@dataclass
class Args:
    phase: str
    input: str
    output: str
    locations: Optional[str]
    diagnostics: Optional[str]
    unknown_args: list[str]


def _parse_args(args: list[str]) -> Args:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="legacy_build")
    parser.add_argument("--input", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--diagnostics", default=None)
    parser.add_argument("--locations", default=None)

    parsed, unknown_args = parser.parse_known_args(args)

    if not parsed.input:
        raise ValueError("Missing required argument --input")

    if not parsed.output:
        raise ValueError("Missing required argument --output")

    return Args(
        phase=parsed.phase,
        input=parsed.input,
        output=parsed.output,
        diagnostics=parsed.diagnostics,
        locations=parsed.locations,
        unknown_args=unknown_args,
    )


def find_modules(package: str) -> list[str]:
    import importlib.util

    spec = importlib.util.find_spec(package)

    if not spec:
        return []

    modules = [
        package + "." + module.name
        for module in pkgutil.iter_modules(path=spec.submodule_search_locations)
        # this will filter out nested packages, since we already find them using
        # find_packages
        if not module.ispkg
    ]

    return modules


def _load_module_names_from_includes(
    includes: list[str],
) -> tuple[list[str], Diagnostics]:
    diagnostics = Diagnostics()
    all_module_names = []

    for import_package in includes:
        module_names, diagnostics = diagnostics.extend_tuple(
            _load_module_names_from_import_package(import_package)
        )

        all_module_names.extend(module_names)

        if diagnostics.has_error():
            return [], diagnostics

    all_module_names = list(set(all_module_names))
    all_module_names.sort()

    return all_module_names, diagnostics


def _load_module_names_from_import_package(
    import_package: str,
) -> tuple[list[str], Diagnostics]:
    package_spec = importlib.util.find_spec(import_package)
    diagnostics = Diagnostics()
    module_names = []

    if not package_spec:
        return [], Diagnostics.create_error(
            f"Package '{import_package}' was not found",
        )

    if package_spec.origin:
        module_names.append(package_spec.name)

    if package_spec.submodule_search_locations:
        package_paths = package_spec.submodule_search_locations
        prefix = import_package + "."

        for loader, module_name, is_pkg in pkgutil.walk_packages(package_paths, prefix):
            module_names.append(module_name)

    module_names.sort()  # create deterministic order

    return module_names, diagnostics


def _find_imports(bundle: dict):
    packages = bundle.get("experimental", {}).get("pydabs", {}).get("import", None)

    if packages is not None:
        return packages

    packages = bundle.get("python", {}).get("import", None)

    if packages is not None:
        return packages

    return None


def main(args: Args) -> Diagnostics:
    diagnostics = Diagnostics()
    bundle = json.load(open(args.input))

    imports = _find_imports(bundle)

    if imports is None:
        return diagnostics.extend(
            Diagnostics.create_error(
                msg="Since PyDABs 0.5.1 'import' option and Databricks CLI 0.227.1+ is required",
                detail="\n".join(
                    [
                        "Example:",
                        "",
                        "experimental:",
                        "  pydabs:",
                        "    enabled: true",
                        "    import:",
                        "    - my_module",
                        "",
                        "Specified packages are imported to discover resources, resource generators, and mutators. ",
                        "This list can include namespace packages, which causes the import of nested packages.",
                    ]
                ),
            )
        )

    module_names, diagnostics = diagnostics.extend_tuple(
        _load_module_names_from_includes(imports)
    )

    if diagnostics.has_error():
        return diagnostics

    # if discovery fails, we have a potential to destroy resources
    # let's be safe and exit if it doesn't look correct
    if not module_names:
        return diagnostics.extend(
            Diagnostics.create_error(
                "No Python modules found, check your configuration"
            )
        )

    if diagnostics.has_error():
        return diagnostics

    try:
        if args.phase == "load":
            loader, diagnostics = diagnostics.extend_tuple(
                _load_bundle(bundle, module_names, only_load=True)
            )

            if not diagnostics.has_error():
                _update_bundle(bundle, loader)

            with open(args.output, "w") as f:
                json.dump(bundle, f)

            if args.locations:
                with open(args.locations, "w") as f:
                    _write_locations(f, loader)

            return diagnostics
        elif args.phase == "init":
            # clear all warnings, because they are already reported at 'load' stage
            diagnostics = Diagnostics()

            loader, diagnostics = diagnostics.extend_tuple(
                _load_bundle(bundle, module_names, only_load=False)
            )

            if not diagnostics.has_error():
                _update_bundle(bundle, loader)

            with open(args.output, "w") as f:
                json.dump(bundle, f)

            if args.locations:
                with open(args.locations, "w") as f:
                    _write_locations(f, loader)

            return diagnostics
        else:
            return diagnostics.extend(
                Diagnostics.create_error(f"Unknown phase '{args.phase}'")
            )
    except Exception as exc:
        return diagnostics.extend(
            Diagnostics.from_exception(
                summary="Unhandled exception in Python mutator",
                exc=exc,
            )
        )


def _legacy_print_diagnostics(diagnostics: Diagnostics):
    for diagnostic in diagnostics.items:
        log_fn = (
            logging.error if diagnostic.severity == Severity.ERROR else logging.warning
        )

        log_fn(f"{diagnostic.severity.name.upper()}: {diagnostic.summary}")
        if diagnostic.detail:
            log_fn(f"{diagnostic.detail}")
        if diagnostic.location:
            log_fn(f"at {diagnostic.location.to_text()}")


if __name__ == "__main__":
    args = _parse_args(sys.argv[1:])

    if args.unknown_args:
        logging.warning(f"Unknown arguments: {args.unknown_args}")

    if args.phase == "legacy_build":
        diagnostics = Diagnostics.create_error(
            "PyDABs 0.4.x projects are not supported since PyDABs 0.5.1, upgrade to PyDABs 0.5.1 first "
            "or recreate from the latest template."
        )
    else:
        logging.basicConfig(level=logging.DEBUG, stream=sys.stderr)
        diagnostics = main(args)

    if args.diagnostics:
        with open(args.diagnostics, "w") as f:
            diagnostics.write_json(f)
    else:
        _legacy_print_diagnostics(diagnostics)

    if diagnostics.has_error():
        sys.exit(1)
    else:
        sys.exit(0)
