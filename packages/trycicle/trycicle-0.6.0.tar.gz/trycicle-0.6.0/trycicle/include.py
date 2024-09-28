import dataclasses
import json
import logging
import os
import pathlib
import time

import requests

from .arguments import Arguments
from .models import ComponentInclude
from .subprocess import get_command_output, run_command
from .variables import slugify

logger = logging.getLogger(__name__)

template_repo = "https://gitlab.com/gitlab-org/gitlab.git"
template_path = "lib/gitlab/ci/templates"
template_branch = "master"
template_update_interval = 3600

# This creates a shallow, sparse, blobless clone of the template repository,
# which is faster and uses far less disk space than a full clone.
clone_commands = [
    ["init", "--quiet"],
    ["remote", "add", "origin", template_repo],
    ["sparse-checkout", "set", "--sparse-index", f"{template_path}/"],
]
update_commands = [
    ["fetch", "--quiet", "--depth=1", "--filter=blob:none", "origin", template_branch],
    ["reset", "--quiet", "--hard", f"origin/{template_branch}"],
]


def clone_template_repo(path: pathlib.Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for command in clone_commands:
        run_command(["git", *command], cwd=path, check=True)


def update_template_repo(path: pathlib.Path) -> None:
    if path.exists():
        last_modified = (path / ".git" / "FETCH_HEAD").stat().st_mtime
        if last_modified > time.time() - template_update_interval:
            logger.debug("Template repository was updated recently")
            return
        logger.info("Updating template repository")

    else:
        logger.info("Cloning template repository")
        clone_template_repo(path)

    for command in update_commands:
        run_command(["git", *command], cwd=path, check=True)


@dataclasses.dataclass
class CatalogVersion:
    name: str
    sha: str


ci_catalog_query = """\
query q($projectPath: ID!, $after: String) {
  ciCatalogResource(fullPath: $projectPath) {
    versions(after: $after) {
      pageInfo {
        endCursor
        hasNextPage
      }
      nodes {
        name
        commit {
          sha
        }
      }
    }
  }
}
"""


def get_all_component_versions(
    args: Arguments, component: ComponentInclude
) -> list[CatalogVersion]:
    all_versions = None

    cache_path = (
        args.cache_path
        / "components"
        / f"{component.host}-{component.project_path.replace('/', '-')}.json"
    )
    if cache_path.exists():
        last_modified = cache_path.stat().st_mtime
        if last_modified > time.time() - template_update_interval:
            with cache_path.open() as f:
                try:
                    all_versions = json.load(f)
                except json.JSONDecodeError:
                    pass

    headers = {}
    if gitlab_token := os.environ.get("GITLAB_TOKEN"):
        headers["Authorization"] = f"Bearer {gitlab_token}"

    if all_versions is None:
        all_versions = []
        variables = {"projectPath": component.project_path}
        while True:
            r = requests.post(
                f"https://{component.host}/api/graphql",
                json={"query": ci_catalog_query, "variables": variables},
                headers=headers,
            )
            r.raise_for_status()
            response = r.json()

            if errors := response.get("errors"):
                message = errors[0]["message"]
                if "does not exist" in message:
                    logger.warning(
                        f"Unable to retrieve CI catalog for "
                        f"{component.project_path}: {message}"
                    )
                    break
                raise Exception(message)

            versions = response["data"]["ciCatalogResource"]["versions"]
            all_versions += [
                {"name": version["name"], "sha": version["commit"]["sha"]}
                for version in versions["nodes"]
            ]

            if not versions["pageInfo"]["hasNextPage"]:
                break
            variables["after"] = versions["pageInfo"]["endCursor"]

        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with cache_path.open("w") as f:
            json.dump(all_versions, f)

    return [CatalogVersion(**version) for version in all_versions]


def version_match(version: str, component: ComponentInclude) -> bool:
    return (
        component.is_latest
        or component.version == version
        or (
            component.is_shorthand
            and version.removeprefix("v").startswith(component.version)
        )
    )


def get_component_catalog_version(
    args: Arguments, component: ComponentInclude
) -> CatalogVersion | None:
    all_versions = get_all_component_versions(args, component)
    for version in all_versions:
        if version_match(version.name, component):
            return version
    return None


def get_component_git_sha(path: pathlib.Path, version: str) -> str:
    output = get_command_output(["git", "ls-remote", "origin", version], cwd=path)
    return output.split()[0] if output else version


def get_component_location(
    args: Arguments, component: ComponentInclude
) -> pathlib.Path:
    path_slug = slugify(component.project_path)
    version_slug = slugify(component.version)
    path = (
        args.cache_path / "components" / f"{component.host}-{path_slug}-{version_slug}"
    )

    if not path.exists():
        logger.info(f"Cloning component repository {component.project_path}")
        path.mkdir(parents=True, exist_ok=True)
        run_command(
            [
                "git",
                "clone",
                "--quiet",
                "--depth=1",
                f"git@{component.host}:{component.project_path}.git",
                ".",
            ],
            cwd=path,
            check=True,
        )

    if catalog_version := get_component_catalog_version(args, component):
        sha = catalog_version.sha
        logger.debug(
            f"{component.project_path} version {catalog_version.name} resolved to {sha}"
        )
    else:
        sha = get_component_git_sha(path, component.version)
        logger.debug(
            f"No catalog version of {component.project_path} "
            f"matched {component.version}, using {sha}"
        )

    if get_command_output(["git", "rev-parse", "HEAD"], cwd=path) != sha:
        run_command(["git", "fetch", "--quiet", "origin", sha], cwd=path, check=True)
        run_command(["git", "reset", "--quiet", "--hard", sha], cwd=path, check=True)

    return path
