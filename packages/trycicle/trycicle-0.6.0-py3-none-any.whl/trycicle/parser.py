import copy
import io
import pathlib
import shlex
import typing
from collections import deque

import requests
import yaml

from .arguments import Arguments
from .glob import glob
from .include import (
    get_component_location,
    template_path,
    update_template_repo,
)
from .interpolation import Context, interpolate
from .models import (
    Cache,
    ComponentInclude,
    Config,
    Dict,
    Include,
    IncludeSource,
    Input,
    Job,
    JobImage,
    Matrix,
    ProjectInclude,
    Reference,
    Service,
)

NOT_JOBS = {"workflow", "stages"}

T = typing.TypeVar("T")


def get_list(v: T | list[T] | None) -> list[T]:
    if v is None:
        return []
    if isinstance(v, list):
        return v
    return [v]


def get_list_or_none(v: T | list[T] | None) -> list[T] | None:
    if isinstance(v, list):
        return v
    return [v] if v is not None else None


def parse_command(raw: str | list[str] | None) -> list[str] | None:
    if raw is None:
        return None
    return shlex.split(raw) if isinstance(raw, str) else raw


def parse_service(raw: typing.Any) -> Service:
    if isinstance(raw, str):
        raw = {"name": raw}
    if isinstance(raw, dict):
        alias, _, _ = raw["name"].replace("/", "-").partition(":")
        return Service(
            name=raw["name"],
            alias=raw.get("alias") or alias,
            variables=raw.get("variables"),
            entrypoint=parse_command(raw.get("entrypoint")),
            command=parse_command(raw.get("command")),
        )
    raise ValueError(f"Unable to parse service, expected str or dict, got {raw!r}")


def parse_image(raw: typing.Any) -> JobImage:
    if isinstance(raw, str):
        return JobImage(name=raw)
    if isinstance(raw, dict):
        if "entrypoint" in raw:
            raw["entrypoint"] = get_list_or_none(raw["entrypoint"])
        return JobImage(**raw)
    raise ValueError(f"Unable to parse image, expected str or dict, got {raw!r}")


def parse_cache(raw: Dict) -> Cache:
    raw_key = raw.get("key") or "default"
    if isinstance(raw_key, str):
        key = raw_key
        key_files = None
        key_prefix = None
    else:
        key = None
        key_files = raw_key.get("files")
        assert isinstance(key_files, list)
        assert 1 <= len(key_files) <= 2
        key_prefix = raw_key.get("prefix")

    return Cache(
        key=key,
        key_files=key_files,
        key_prefix=key_prefix,
        paths=raw.get("paths"),
        untracked=raw.get("untracked", False),
        when=raw.get("when", "on_success"),
        policy=raw.get("policy", "pull-push"),
    )


def parse_parallel(raw: typing.Any) -> int | Matrix | None:
    if raw is None:
        return None
    if isinstance(raw, int):
        return raw
    if isinstance(raw, dict) and (matrix := raw.get("matrix")):
        return Matrix(
            [{key: get_list(value) for key, value in item.items()} for item in matrix]
        )
    raise ValueError(f"Unable to parse parallel, expected int or matrix, got {raw!r}")


def parse_job(name: str, raw: Dict) -> Job:
    image = parse_image(raw["image"])
    before_script: list[str] = get_list(raw.get("before_script"))
    script: list[str] = get_list(raw.get("script"))
    after_script: list[str] = get_list(raw.get("after_script"))
    variables = {k: str(v) for k, v in raw.get("variables", {}).items()}
    raw_services: list[typing.Any] = get_list(raw.get("services"))
    services = [parse_service(s) for s in raw_services]
    raw_cache: list[Dict] = get_list(raw.get("cache"))
    cache = [parse_cache(c) for c in raw_cache]
    parallel = parse_parallel(raw.get("parallel"))
    return Job(
        name=name,
        image=image,
        before_script=before_script,
        script=script,
        after_script=after_script,
        variables=variables,
        services=services,
        cache=cache,
        parallel=parallel,
    )


def parse_include(raw: typing.Any) -> Include:
    if isinstance(raw, str):
        source: IncludeSource = (
            "remote"
            if raw.startswith("http://") or raw.startswith("https://")
            else "local"
        )
        return Include(source=source, location=raw, inputs={})

    if isinstance(raw, dict):
        inputs = raw.get("inputs") or {}
        if "project" in raw:
            return ProjectInclude(
                source="project",
                location=raw["project"],
                file=raw["file"],
                ref=raw.get("ref", "HEAD"),
                inputs=inputs,
            )
        for source in typing.get_args(IncludeSource):
            if source in raw:
                return Include(source=source, location=raw[source], inputs=inputs)

        keys = ", ".join(f"{source!r}" for source in typing.get_args(IncludeSource))
        raise ValueError(
            f"Unable to parse include, expected one of {keys}; got {raw!r}"
        )

    raise ValueError(f"Unable to parse include, expected str or dict, got {raw!r}")


def parse_input(raw: typing.Any) -> Input:
    if raw is None:
        return Input(type="string")
    if isinstance(raw, dict):
        return Input(
            default=raw.get("default"),
            options=raw.get("options"),
            regex=raw.get("regex"),
            type=raw.get("type", "string"),
        )
    raise ValueError(f"Unable to parse input, expected dict, got {raw!r}")


def extend(a: Dict, b: Dict) -> Dict:
    """Extend `a` with values from `b`. Values in `a` will not be overwritten."""
    merged = copy.deepcopy(a)
    for key, value in b.items():
        if key not in a:
            merged[key] = value
        elif isinstance(a[key], dict) and isinstance(value, dict):
            merged[key] = extend(a[key], value)
    return merged


def all_parents(config: Dict, name: str) -> typing.Iterable[str]:
    """Get all parents of a job, including the job itself."""
    parents = deque([name])
    while parents:
        parent = parents.popleft()
        yield parent
        parents.extendleft(get_list(config[parent].get("extends")))


def merge_extends_and_defaults(
    name: str, config: Dict, default: Dict, globals: Dict, variables: dict[str, str]
) -> Dict:
    job: Dict = {"variables": {}}

    # Merge job with all extends
    for parent in all_parents(config, name):
        job = extend(job, config[parent])

    # Merge job with defaults, respecting `inherit:default`
    inherit = job.get("inherit", {})
    inherit_default = inherit.get("default", True)
    if isinstance(inherit_default, list):
        for key in inherit_default:
            if key in default and key not in job:
                job[key] = default[key]
    elif inherit_default:
        job = extend(job, default)

    # Merge job with variables, respecting `inherit:variables`
    inherit_variables = inherit.get("variables", True)
    if isinstance(inherit_variables, list):
        for key in inherit_variables:
            if key in variables and key not in job["variables"]:
                job["variables"][key] = variables[key]
    elif inherit_variables:
        job["variables"] = extend(job["variables"], variables)

    # Merge job with globals
    return extend(job, globals)


def resolve_references(root: Dict, value: typing.Any) -> typing.Any:
    if isinstance(value, Reference):
        resolved = root
        for key in value.path:
            resolved = resolved[key]
        return resolve_references(root, resolved)

    if isinstance(value, dict):
        return {k: resolve_references(root, v) for k, v in value.items()}

    if isinstance(value, list):
        new_value = []
        for item in value:
            # Flatten references that resolve to another list, but not nested lists
            resolved = resolve_references(root, item)
            if isinstance(item, Reference) and isinstance(resolved, list):
                new_value.extend(resolved)
            else:
                new_value.append(resolved)

        return new_value

    return value


def construct_reference(self: yaml.SafeLoader, node: yaml.SequenceNode) -> Reference:
    return Reference(self.construct_sequence(node))


yaml.SafeLoader.add_constructor("!reference", construct_reference)


def load_config_and_spec(fp: typing.TextIO) -> tuple[Dict, Dict | None]:
    documents = yaml.safe_load_all(fp)

    # We expect either one or two documents in the file.
    try:
        first = next(documents)
    except StopIteration:
        raise ValueError("Configuration is empty")
    assert isinstance(first, dict)

    try:
        second = next(documents)
    except StopIteration:
        return first, None
    assert isinstance(second, dict)

    try:
        next(documents)
    except StopIteration:
        pass
    else:
        raise ValueError("Too many documents in configuration")

    # If there are two, the first should contain a spec.
    assert "spec" in first
    return second, first


# In GitLab CI, the maximum number of included files for a pipeline is 150.
max_includes = 150


def load(
    fp: typing.TextIO,
    path: pathlib.Path | None,
    input_values: dict[str, typing.Any],
    args: Arguments,
) -> typing.Iterable[Dict]:
    raw, spec = load_config_and_spec(fp)
    if spec is not None:
        context = Context(inputs={}, variables=args.variables)
        for name, raw_input in spec["spec"].get("inputs", {}).items():
            input_spec = parse_input(raw_input)
            if name in input_values:
                context.inputs[name] = input_values[name]
            elif input_spec.default is not None:
                context.inputs[name] = input_spec.default
            else:
                raise ValueError(f"Missing required input {name!r}")

        raw = interpolate(context, raw)

    yield raw

    # From https://docs.gitlab.com/ee/ci/yaml/includes.html#merge-method-for-include
    # * Included files are read in the order defined in the configuration file,
    #   and the included configuration is merged together in the same order.
    # * If an included file also uses include, that nested include configuration
    #   is merged first (recursively).
    for raw_include in get_list(raw.get("include")):  # type: typing.Any
        include = parse_include(raw_include)
        yield from load_include(include, path, args)


def load_include(
    include: Include, path: pathlib.Path | None, args: Arguments
) -> typing.Iterable[Dict]:
    include_location = args.variables.replace(include.location)
    match include.source:
        case "local":
            if path is None:
                raise ValueError("Cannot include local file without path")
            for location in glob(path, include_location):
                with open(location) as fp:
                    yield from load(fp, location.parent, include.inputs, args)

        case "remote":
            # All nested includes are executed without context as a public user.
            # No variables are available in the include section of nested includes.
            r = requests.get(include_location)
            r.raise_for_status()
            yield from load(
                io.StringIO(r.text), None, include.inputs, args.without_variables()
            )

        case "template":
            template_repo = args.cache_path / "templates"
            update_template_repo(template_repo)
            location = template_repo / template_path / include_location
            with open(location) as fp:
                yield from load(fp, location.parent, include.inputs, args)

        case "component":
            component = ComponentInclude(location=include_location)
            repo_path = get_component_location(args, component)
            location = repo_path / "templates" / f"{component.name}.yml"
            with open(location) as fp:
                yield from load(fp, repo_path, include.inputs, args)

        case _:
            raise NotImplementedError(f"include:{include.source} not implemented")


def load_config(fp: typing.TextIO, args: Arguments) -> Dict:
    try:
        path = pathlib.Path(fp.name).parent
    except AttributeError:
        path = None

    merged: Dict = {}
    for i, raw in enumerate(load(fp, path, input_values={}, args=args)):
        if i > max_includes:
            raise Exception("Too many includes")
        merged = extend(merged, raw)

    merged = resolve_references(merged, merged)
    assert isinstance(merged, dict)
    return merged


def parse_config(fp: typing.TextIO, args: Arguments | None = None) -> Config:
    raw = load_config(fp, args or Arguments())

    # Globally set defaults (deprecated, but widely used)
    globals = {
        key: raw.pop(key)
        for key in ("image", "services", "cache", "before_script", "after_script")
        if key in raw
    }

    default = raw.pop("default", {})

    # Global variables support some extra options, but we only need the values
    variables = {
        key: str(value.get("value", "")) if isinstance(value, dict) else str(value)
        for key, value in raw.pop("variables", {}).items()
    }

    return Config(
        globals=globals,
        default=default,
        variables=variables,
        jobs={
            key: value
            for key, value in raw.items()
            if isinstance(value, dict) and key not in NOT_JOBS
        },
    )
