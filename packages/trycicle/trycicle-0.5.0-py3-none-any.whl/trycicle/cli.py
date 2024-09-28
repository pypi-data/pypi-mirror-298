import logging
import os
import pathlib
import sys
import typing

import click
from click.shell_completion import CompletionItem

from .arguments import Arguments, DebugEnabled
from .models import Config, Job
from .parser import parse_config
from .run import run_job


def parse_ctx(ctx: click.Context) -> Config | None:
    file = ctx.params.get("file")
    if not file:
        return None

    args = Arguments(
        original_dir=ctx.params.get("workdir") or pathlib.Path(file.name).parent,
        cache_directory=ctx.params.get("cache_directory"),
    )
    try:
        return parse_config(file, args)
    except Exception:  # TODO: Use specific exceptions
        return None


def complete_variables(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    if "=" in incomplete:
        return []

    if config := parse_ctx(ctx):
        variable_names = config.all_variable_names()
    else:
        variable_names = set()

    variables = [
        CompletionItem(k, help="Variable")
        for k in sorted(variable_names)
        if k.startswith(incomplete)
    ]

    environment = [
        CompletionItem(k, help="Environment")
        for k in sorted(os.environ)
        if k.startswith(incomplete)
    ]
    return variables + environment


def complete_job(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[CompletionItem]:
    if not ctx.params["file"]:
        return []

    config = parse_ctx(ctx)
    if not config:
        return []

    return [
        CompletionItem(name, help="Job")
        for name in sorted(config.jobs)
        if name.startswith(incomplete)
        and (incomplete.startswith(".") or not name.startswith("."))
    ]


@click.command(name="trycicle")
@click.option(
    "--verbose",
    "-v",
    count=True,
    help="Verbose output",
)
@click.option(
    "--service-logs/--no-service-logs",
    default=False,
    help="Display logs from services",
)
@click.option(
    "--workdir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, path_type=pathlib.Path
    ),
    metavar="DIR",
    help="Working directory",
)
@click.option(
    "--clean/--in-place",
    default=False,
    help="Run in a clean copy of the repository",
)
@click.option(
    "--env",
    "-e",
    metavar="KEY[=VALUE]",
    multiple=True,
    help="Environment variables to pass to the job",
    shell_complete=complete_variables,
)
@click.option(
    "--file",
    "-f",
    type=click.File("r"),
    metavar="YAML",
    help="Path to the .gitlab-ci.yml file",
    default=".gitlab-ci.yml",
)
@click.option(
    "--debug",
    type=click.Choice(("true", "false", "immediate"), case_sensitive=False),
    is_flag=False,
    flag_value="true",
    default="false",
    help="Enable interactive debugging",
)
@click.option(
    "--cache-directory",
    type=click.Path(file_okay=False, dir_okay=True, path_type=pathlib.Path),
    metavar="DIR",
    help="Directory to store cache files",
)
@click.argument(
    "job_name",
    metavar="JOB",
    required=False,
    shell_complete=complete_job,
)
def main(
    verbose: int,
    service_logs: bool,
    workdir: pathlib.Path | None,
    clean: bool,
    env: list[str],
    file: typing.TextIO,
    job_name: str | None,
    debug: DebugEnabled,
    cache_directory: pathlib.Path | None,
) -> None:
    configure_logging(verbose)

    args = Arguments(
        original_dir=workdir or pathlib.Path(file.name).parent,
        service_logs=service_logs,
        debugger=debug,
        cache_directory=cache_directory,
        clean_copy=clean,
    )

    config = parse_config(file, args)
    if job_name not in config.jobs:
        error = job_name is not None
        if error:
            click.echo(f"Job {job_name!r} not found in {file!r}", err=True)
        click.echo("Available jobs:", err=error)
        for name in config.jobs:
            if not name.startswith("."):
                click.echo(f"  - {name}", err=error)
        sys.exit(1 if error else 0)

    job = config.get_job(job_name)

    if job.parallel and args.interactive:
        click.echo("Cannot run a parallel job with debugger", err=True)
        click.echo(
            "Hint: comment out the 'parallel' key in the job definition "
            "and pass variables with -e/--env",
            err=True,
        )
        sys.exit(1)

    set_variables(job, env)
    result = run_job(job, args)
    sys.exit(result)


def configure_logging(verbose: int) -> None:
    logging.basicConfig(level=logging.INFO)
    if verbose >= 2:
        logging.getLogger().setLevel(logging.DEBUG)
    elif verbose:
        logging.getLogger(__package__).setLevel(logging.DEBUG)


def set_variables(job: Job, variables: list[str]) -> None:
    for variable in variables:
        if "=" in variable:
            key, value = variable.split("=", 1)
        else:
            key, value = variable, os.environ[variable]
        job.variables[key] = value
