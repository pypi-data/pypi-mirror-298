import logging
import pathlib
import shutil
import tempfile
import typing

from .subprocess import get_command_output, run_command

logger = logging.getLogger(__name__)


def create_clean_copy(source_dir: pathlib.Path) -> pathlib.Path:
    toplevel = get_command_output(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=source_dir,
    )

    clone_dir = pathlib.Path(tempfile.mkdtemp())
    clone_dir.chmod(0o755)

    run_command(["git", "clone", "--local", toplevel, str(clone_dir)], check=True)
    run_command(
        ["git", "remote", "set-url", "origin", "/repo"], cwd=clone_dir, check=True
    )

    return clone_dir / source_dir.relative_to(toplevel)


def remove_copy(clone_dir: pathlib.Path) -> None:
    status = get_command_output(
        ["git", "status", "--porcelain"],
        cwd=clone_dir,
    )
    if status:
        logger.warning(f"Some files in {clone_dir!r} have been changed")
        return

    toplevel = get_command_output(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=clone_dir,
    )
    rmtree_warn_errors(pathlib.Path(toplevel))


def rmtree_warn_errors(path: pathlib.Path) -> None:
    errors = 0

    def onerror(*args: typing.Any) -> None:
        nonlocal errors
        errors += 1

    shutil.rmtree(path, onerror=onerror)
    if errors:
        logger.warning(f"Unable to remove {errors} files from {path!r}")
