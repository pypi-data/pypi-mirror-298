import dataclasses
import itertools
import logging
import pathlib
import shutil
import sys
import tempfile
import threading
import typing
from datetime import UTC, datetime

from docker import DockerClient
from docker.errors import ImageNotFound
from docker.models.containers import Container

from .arguments import Arguments, DebugEnabled
from .cache import get_cache_path, pull_cache, push_cache
from .git_clone import create_clean_copy, remove_copy
from .models import Job, Service
from .subprocess import run_command
from .variables import Variables, get_job_variables

logger = logging.getLogger(__name__)

job_script_shebang = "#!/bin/sh\n"

job_script_header = """\
git config --global --add safe.directory /src 2>/dev/null || true
set -ex
"""

job_script_debugger = """\
# Start a shell if the script fails
function debugger() {
    set +x
    if [ -n "$1" ]; then
       echo "Job failed, starting debug shell." >&2
       echo "Last command: $BASH_COMMAND" >&2
    fi
    echo "The job script is available at $0" >&2
    echo "The job will continue after you exit this shell. To abort, type 'exit 1'" >&2
    ${SHELL:-sh} || exit 1
    set -x
}
trap 'debugger trap' ERR
"""


def write_job_script(
    path: pathlib.Path,
    before_script: list[str],
    script: list[str],
    debugger: DebugEnabled = "false",
) -> None:
    with path.open("w") as fp:
        print(job_script_shebang.strip(), file=fp)
        if debugger != "false":
            print(job_script_debugger.strip(), file=fp)
        print(job_script_header.strip(), file=fp)
        if debugger == "immediate":
            print("debugger", file=fp)
        if before_script:
            print("", file=fp)
            print("# Before", file=fp)
            print("\n".join(before_script), file=fp)
        if script:
            print("", file=fp)
            print("# Script", file=fp)
            print("\n".join(script), file=fp)
    path.chmod(0o755)


dind_volumes = {"dind-certs": {"bind": "/certs/client", "mode": "rw"}}


@dataclasses.dataclass
class Run:
    docker: DockerClient
    job: Job
    args: Arguments

    start: datetime = dataclasses.field(default_factory=lambda: datetime.now(UTC))

    build_dir: pathlib.Path = dataclasses.field(init=False)
    variables: Variables = dataclasses.field(init=False)
    labels: dict[str, str] = dataclasses.field(init=False)
    links: dict[str, str] = dataclasses.field(init=False)
    stop_event_thread: typing.Callable[[], None] | None = None
    service_containers: list[Container] = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        args = self.args

        self.build_dir = pathlib.Path(tempfile.mkdtemp())
        self.build_dir.chmod(0o755)
        logger.debug(f"Using temporary build directory {self.build_dir}")

        job_sh = self.build_dir / "job.sh"
        write_job_script(job_sh, self.job.before_script, self.job.script, args.debugger)

        self.variables = args.variables + get_job_variables(self.job)

        self.labels = {
            "trycicle": "true",
            "trycicle.workdir": str(args.original_dir),
            "trycicle.job": self.job.name,
        }

        self.service_containers = [
            run_service(
                self.docker, service, self.variables, self.labels, args.service_logs
            )
            for service in self.job.services
        ]
        self.links = {
            container.id: service.alias
            for service, container in zip(self.job.services, self.service_containers)
        }

        if self.service_containers:
            self.stop_event_thread = start_event_thread(
                self.docker, self.links, self.start
            )

    def cleanup(self) -> None:
        # TODO: Remove containers? (on success only?)

        if self.stop_event_thread:
            self.stop_event_thread()

        if self.service_containers:
            logger.debug(f"Stopping {len(self.service_containers)} service containers")
            for container in self.service_containers:
                container.stop()

        shutil.rmtree(self.build_dir)


@dataclasses.dataclass
class RunJob:
    run: Run
    name: str
    variables: Variables

    source_dir: pathlib.Path = dataclasses.field(init=False)
    cache_paths: list[pathlib.Path] = dataclasses.field(init=False)
    container: Container = dataclasses.field(init=False)

    def __post_init__(self) -> None:
        args = self.run.args
        job = self.run.job

        if args.clean_copy:
            self.source_dir = create_clean_copy(args.original_dir)
        else:
            self.source_dir = args.original_dir

        volumes = {
            str(self.source_dir): {"bind": "/src", "mode": "rw"},
            str(self.run.build_dir): {"bind": "/build", "mode": "ro"},
        }

        if args.clean_copy:
            volumes[str(args.original_dir)] = {"bind": "/repo", "mode": "ro"}

        if any(service.is_docker_dind for service in job.services):
            volumes.update(dind_volumes)

        self.cache_paths = [
            args.cache_path / get_cache_path(cache, self.variables, args.original_dir)
            for cache in job.cache
        ]
        for cache_path, cache in zip(self.cache_paths, job.cache):
            pull_cache(cache, self.variables, cache_path, self.source_dir)

        job_image = self.variables.replace(job.image.name)
        logger.info(f"Starting job {self.name} ({job_image})")

        self.container = create_container(
            self.run.docker,
            image=job_image,
            detach=True,
            tty=True,
            stdin_open=args.interactive,
            command=["/build/job.sh"],
            entrypoint=self.variables.replace_list(job.image.entrypoint),
            environment=self.variables.as_dict(),
            volumes=volumes,
            links=self.run.links,
            working_dir="/src",
            labels=self.run.labels,
        )

        if job.parallel:
            self.container.start()
            start_log_thread(self.container, f"{self.name} | ".encode())
        elif args.interactive:
            interactive_session(self.container)
        else:
            self.container.start()
            write_logs(self.container, b"job | " if args.service_logs else b"")

    def wait(self) -> int:
        status_code = int(self.container.wait()["StatusCode"])
        logger.debug(f"Job {self.name} finished with exit code {status_code}")

        for cache_path, cache in zip(self.cache_paths, self.run.job.cache):
            if (
                cache.when == "always"
                or (cache.when == "on_success" and status_code == 0)
                or (cache.when == "on_failure" and status_code != 0)
            ):
                push_cache(cache, self.variables, cache_path, self.source_dir)

        if self.run.args.clean_copy:
            remove_copy(self.source_dir)

        return status_code


def run_job(job: Job, args: Arguments) -> int:
    docker = DockerClient.from_env()
    run = Run(docker, job, args)

    jobs = [
        RunJob(run, name, run.variables + variables)
        for name, variables in generate_parallel(job)
    ]

    status_code = max(j.wait() for j in jobs)

    run.cleanup()

    return status_code


def write_logs(container: Container, prefix: bytes = b"") -> None:
    """Write logs from a container to stdout, optionally prefixing every line.

    Because this function is called from multiple threads, it internally buffers the
    logs until a newline is found, to avoid mixing output from different containers.
    """
    buffer = b""
    for chunk in container.logs(stream=True, follow=True):
        buffer += chunk
        if not buffer:
            continue

        # Split the accumulated buffer into lines. If the last line is complete, output
        # everything. Otherwise, keep the last line in the buffer, and output the rest.
        lines = buffer.splitlines(keepends=True)
        if lines[-1].endswith(b"\n"):
            buffer = b""
        else:
            buffer = lines.pop()

        for line in lines:
            sys.stdout.buffer.write(prefix + line)
            sys.stdout.flush()

    # Output the last line, if any.
    if buffer:
        sys.stdout.buffer.write(prefix + buffer + b"\n")


def start_log_thread(container: Container, prefix: bytes = b"") -> None:
    thread = threading.Thread(
        target=write_logs,
        args=(container, prefix),
        daemon=True,
    )
    thread.start()


def create_container(docker: DockerClient, **kwargs: typing.Any) -> Container:
    try:
        return docker.containers.create(**kwargs)
    except ImageNotFound:
        docker.images.pull(kwargs["image"])
        return docker.containers.create(**kwargs)


def run_service(
    docker: DockerClient,
    service: Service,
    variables: Variables,
    labels: dict[str, str],
    logs: bool,
) -> Container:
    service_variables = variables + service.variables
    service_image = service_variables.replace(service.name)

    volumes = {}
    if service.is_docker_dind:
        volumes.update(dind_volumes)

    logger.info(f"Starting service {service.alias} ({service_image})")
    container = create_container(
        docker,
        image=service_image,
        detach=True,
        command=service_variables.replace_list(service.command),
        entrypoint=service_variables.replace_list(service.entrypoint),
        environment=service_variables.as_dict(),
        privileged=service.is_docker_dind,
        volumes=volumes,
        labels={"trycicle.service": service.alias, **labels},
    )
    container.start()

    if logs:
        start_log_thread(container, f"{service.alias} | ".encode())

    return container


def start_event_thread(
    docker: DockerClient, containers: dict[str, str], since: datetime
) -> typing.Callable[[], None]:
    # We're only interested in events for the services
    filters = {
        "type": ["container"],
        "container": list(containers.keys()),
    }
    event_stream = docker.events(filters=filters, since=since, decode=True)

    thread = threading.Thread(
        target=consume_events,
        args=(event_stream, containers),
        daemon=True,
    )
    thread.start()

    return event_stream.close  # type: ignore[no-any-return]


class DockerEventActor(typing.TypedDict):
    ID: str
    Attributes: dict[str, str]


class DockerEvent(typing.TypedDict):
    Type: str
    Action: str
    Actor: DockerEventActor
    scope: str
    time: int
    timeNano: int


def consume_events(
    stream: typing.Iterable[DockerEvent], containers: dict[str, str]
) -> None:
    unhealthy: set[str] = set()

    for event in stream:
        alias = containers.get(event["Actor"]["ID"])
        if alias is None:
            continue

        match event["Action"]:
            case "die":
                status = event["Actor"]["Attributes"]["exitCode"]
                verb = "finished" if status == "0" else "died"
                logger.warning(f"Service {alias} {verb} with exit code {status}")
            case "oom":
                logger.warning(f"Service {alias} ran out of memory")
            case "health_status: healthy":
                if alias in unhealthy:
                    logger.info(f"Service {alias} is healthy")
                    unhealthy.remove(alias)
            case "health_status: unhealthy":
                if alias not in unhealthy:
                    logger.warning(f"Service {alias} is unhealthy")
                    unhealthy.add(alias)


def interactive_session(container: Container) -> None:
    # Unfortunately, docker-py doesn't seem to support interactively attaching
    # to a running container, so we have to shell out.
    run_command(["docker", "start", "--attach", "--interactive", container.id])


def generate_parallel(job: Job) -> typing.Iterable[tuple[str, dict[str, str]]]:
    if not job.parallel:
        yield job.name, {}

    elif isinstance(job.parallel, int):
        for i in range(1, job.parallel + 1):
            yield (
                f"{job.name} {i}/{job.parallel}",
                {"CI_NODE_INDEX": f"{i}", "CI_NODE_TOTAL": f"{job.parallel}"},
            )

    else:
        for variables in job.parallel.variables:
            options = [
                [(key, value) for value in values] for key, values in variables.items()
            ]
            for pairs in itertools.product(*options):
                label = ", ".join(value for _, value in pairs)
                yield f"{job.name} [{label}]", dict(pairs)
