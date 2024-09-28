import dataclasses
import re
import typing

Dict: typing.TypeAlias = dict[str, typing.Any]


@dataclasses.dataclass
class Reference:
    path: list[str]


@dataclasses.dataclass
class Service:
    name: str
    alias: str
    variables: dict[str, str] | None = None
    entrypoint: list[str] | None = None
    command: list[str] | None = None

    @property
    def is_docker_dind(self) -> bool:
        return self.name.startswith("docker:") and "dind" in self.name


@dataclasses.dataclass
class JobImage:
    name: str
    entrypoint: list[str] | None = None


@dataclasses.dataclass
class Cache:
    key: str | None = None
    key_files: list[str] | None = None
    key_prefix: str | None = None
    paths: list[str] | None = None  # Array of globs relative to CI_PROJECT_DIR
    untracked: bool = False
    when: typing.Literal["on_success", "on_failure", "always"] = "on_success"
    policy: typing.Literal["pull", "push", "pull-push"] = "pull-push"


@dataclasses.dataclass
class Matrix:
    variables: list[dict[str, list[str]]]


@dataclasses.dataclass
class Job:
    name: str
    image: JobImage
    before_script: list[str] = dataclasses.field(default_factory=list)
    script: list[str] = dataclasses.field(default_factory=list)
    after_script: list[str] = dataclasses.field(default_factory=list)
    variables: dict[str, str] = dataclasses.field(default_factory=dict)
    services: list[Service] = dataclasses.field(default_factory=list)
    cache: list[Cache] = dataclasses.field(default_factory=list)
    parallel: int | Matrix | None = None


IncludeSource = typing.Literal["component", "local", "project", "remote", "template"]


@dataclasses.dataclass
class Include:
    source: IncludeSource
    location: str
    inputs: dict[str, typing.Any]


@dataclasses.dataclass
class ProjectInclude(Include):
    file: str
    ref: str


@dataclasses.dataclass
class ComponentInclude:
    location: str
    host: str = dataclasses.field(init=False)
    project_path: str = dataclasses.field(init=False)
    name: str = dataclasses.field(init=False)
    version: str = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        address, self.version = self.location.split("@")
        self.host, path = address.split("/", 1)
        self.project_path, self.name = path.rsplit("/", 1)

    @property
    def is_latest(self) -> bool:
        return self.version == "~latest"

    @property
    def is_shorthand(self) -> bool:
        return re.fullmatch(r"\d+(\.\d+)?", self.version) is not None


@dataclasses.dataclass
class Input:
    default: typing.Any = None
    options: list[str] | None = None
    regex: str | None = None
    type: typing.Literal["string", "array", "number", "boolean"] = "string"


@dataclasses.dataclass
class Config:
    globals: Dict
    default: Dict
    variables: dict[str, str]
    jobs: Dict

    def get_job(self, name: str) -> Job:
        from .parser import merge_extends_and_defaults, parse_job

        job = merge_extends_and_defaults(
            name, self.jobs, self.default, self.globals, self.variables
        )
        return parse_job(name, job)

    def all_variable_names(self) -> set[str]:
        return set(self.variables.keys()) | {
            name for job in self.jobs.values() for name in job.get("variables", {})
        }
