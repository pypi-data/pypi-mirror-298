import io
import os
import pathlib
import typing
from unittest import mock

import pytest

from trycicle.arguments import Arguments
from trycicle.include import (
    CatalogVersion,
    get_all_component_versions,
    get_component_catalog_version,
    get_component_git_sha,
    get_component_location,
    template_path,
    update_template_repo,
)
from trycicle.models import ComponentInclude, Config
from trycicle.parser import parse_config


@pytest.fixture(name="requests_get", autouse=True)
def mock_requests_get() -> typing.Iterable[mock.Mock]:
    with mock.patch("requests.get", return_value=mock.Mock(text="included: {}")) as m:
        yield m


@pytest.fixture(name="requests_post", autouse=True)
def mock_requests_post() -> typing.Iterable[mock.Mock]:
    with mock.patch("requests.post") as m:
        m.return_value.json.return_value = {}
        yield m


@pytest.fixture(name="update_template_repo", autouse=True)
def mock_update_template_repo() -> typing.Iterable[mock.Mock]:
    with mock.patch("trycicle.parser.update_template_repo") as m:
        yield m


def parse_example(
    example: str, name: str = ".gitlab-ci", **kwargs: typing.Any
) -> Config:
    example_path = pathlib.Path(f"tests/examples/include/{example}")
    args = Arguments(example_path, **kwargs)
    with open(example_path / f"{name}.yml") as fp:
        return parse_config(fp, args)


def test_use_default() -> None:
    config = parse_example("use-default")
    job = config.get_job("rspec1")
    assert job.before_script


def test_include_override() -> None:
    config = parse_example("override")

    job = config.get_job("production")
    assert "POSTGRES_DB" in job.variables
    assert "POSTGRES_USER" in job.variables
    assert job.variables["POSTGRES_DB"] == "$CI_ENVIRONMENT_SLUG"  # from include
    assert job.variables["POSTGRES_USER"] == "root"  # overridden


def test_include_nested_duplicate() -> None:
    config = parse_example("nested-duplicate")

    job = config.get_job("unit-test-job")
    assert job.before_script == ["default-before-script.sh"]
    assert job.script == ["unit-test.sh"]

    job = config.get_job("smoke-test-job")
    assert job.before_script == ["default-before-script.sh"]
    assert job.script == ["smoke-test.sh"]


def test_include_wildcards() -> None:
    config = parse_example("wildcards")

    assert config.jobs.keys() == {"a", "b", "c"}


def test_include_max() -> None:
    with (
        pytest.raises(Exception, match="Too many includes"),
        mock.patch("trycicle.parser.max_includes", 5),
    ):
        parse_example("max")


def test_include_without_path() -> None:
    with pytest.raises(ValueError, match="local file without path"):
        parse_config(io.StringIO("include: pipeline.yml"))


def test_include_remote(requests_get: mock.Mock) -> None:
    url = "https://example.org/pipeline.yml"
    config = parse_config(io.StringIO(f"include: {url}"))
    assert "included" in config.jobs
    requests_get.assert_called_once_with(url)


@pytest.mark.parametrize(
    "source",
    [
        pytest.param("project: test\n    file: some.yml", id="project"),
    ],
)
def test_include_source_not_implemented(source: str) -> None:
    with pytest.raises(NotImplementedError):
        parse_config(io.StringIO(f"include:\n  - {source}"))


def test_include_inputs() -> None:
    config = parse_example("inputs")

    job = config.get_job("scan-website")
    assert job.script == ["./scan-website my-environment"]


def test_include_inputs_missing_required() -> None:
    with pytest.raises(ValueError, match="Missing required input"):
        parse_example("inputs", "missing-required")


def test_include_inputs_same_file_multiple_times() -> None:
    config = parse_example("inputs-same-file-multiple-times")
    assert "run-docs-lint" in config.jobs
    assert "run-yaml-lint" in config.jobs


def test_include_inputs_array() -> None:
    config = parse_example("inputs-array")
    assert config.jobs["test_job"]["rules"] == [
        {"if": '$CI_PIPELINE_SOURCE == "merge_request_event"', "when": "manual"},
        {"if": '$CI_PIPELINE_SOURCE == "schedule"'},
    ]


def test_include_variables(
    requests_get: mock.Mock,
    get_project_variables: mock.Mock,
) -> None:
    project_url = "https://gitlab.example.org/test/project"
    get_project_variables.return_value = {"CI_PROJECT_URL": project_url}

    config = parse_example("variables")

    assert "included" in config.jobs
    requests_get.assert_called_once_with(
        f"{project_url}/-/jobs/1234/artifacts/raw/.gitlab-ci.yml"
    )


@pytest.mark.integration
def test_clone_template_repo(tmp_path: pathlib.Path) -> None:
    repo_path = tmp_path / "repo"
    assert not repo_path.exists()

    update_template_repo(repo_path)
    assert (repo_path / template_path).exists()
    assert (repo_path / template_path / "Code-Quality.gitlab-ci.yml").exists()


@pytest.fixture(name="run_command")
def mock_run_command() -> typing.Iterable[mock.Mock]:
    with mock.patch("trycicle.include.run_command") as m:
        yield m


def test_update_template_repo_clones(
    tmp_path: pathlib.Path, run_command: mock.Mock
) -> None:
    repo_path = tmp_path / "repo"
    assert not repo_path.exists()

    update_template_repo(repo_path)
    assert repo_path.exists()

    run_command.assert_any_call(["git", "init", "--quiet"], cwd=repo_path, check=True)


def test_update_template_repo_cached(
    tmp_path: pathlib.Path, run_command: mock.Mock
) -> None:
    fetch_head = tmp_path / ".git" / "FETCH_HEAD"
    fetch_head.parent.mkdir(parents=True, exist_ok=True)
    fetch_head.touch()

    update_template_repo(tmp_path)
    run_command.assert_not_called()


def test_update_template_repo_out_of_date(
    tmp_path: pathlib.Path, run_command: mock.Mock
) -> None:
    fetch_head = tmp_path / ".git" / "FETCH_HEAD"
    fetch_head.parent.mkdir(parents=True, exist_ok=True)
    fetch_head.touch()

    try:
        os.utime(fetch_head, (0, 0))
    except OSError:
        pytest.skip("Cannot set mtime")

    update_template_repo(tmp_path)
    run_command.assert_called()


def test_include_templates() -> None:
    config = parse_example(
        "templates",
        cache_path=pathlib.Path("tests/examples/include"),
    )
    assert "sast" in config.jobs
    assert "secret_detection" in config.jobs


@pytest.mark.parametrize(
    "version,expected",
    [
        ("~latest", "v2.0.0"),
        ("v1.1.1", "v1.1.1"),
        ("1.1", "v1.1.1"),
        ("1.0", "v1.0.1"),
        ("1", "v1.1.1"),
        ("v1.1.2", ""),
    ],
)
def test_version_match(version: str, expected: str) -> None:
    component = ComponentInclude(f"gitlab.com/project/test@{version}")
    with mock.patch("trycicle.include.get_all_component_versions") as m:
        m.return_value = [
            CatalogVersion("v2.0.0", "5"),
            CatalogVersion("v1.1.1", "4"),
            CatalogVersion("v1.1.0", "3"),
            CatalogVersion("v1.0.1", "2"),
            CatalogVersion("v1.0.0", "1"),
        ]
        result = get_component_catalog_version(mock.Mock(), component)
    assert (
        result is not None and result.name == expected if expected else result is None
    )


ci_catalog_response = {
    "data": {
        "ciCatalogResource": {
            "versions": {
                "pageInfo": {"endCursor": "MTM", "hasNextPage": False},
                "nodes": [
                    {
                        "name": "v1.4.0",
                        "commit": {"sha": "b47a6c16e7e4f43e3bd573f029646464a20316b2"},
                    },
                ],
            },
        }
    }
}

ci_catalog_response_with_next_page = {
    "data": {
        "ciCatalogResource": {
            "versions": {
                "pageInfo": {"endCursor": "MTM", "hasNextPage": True},
                "nodes": [
                    {
                        "name": "v1.3.0",
                        "commit": {"sha": "b47a6c16e7e4f43e3bd573f029646464a20316b2"},
                    },
                ],
            },
        }
    }
}


@pytest.fixture(name="catalog_query")
def mock_catalog_query(requests_post: mock.Mock) -> mock.Mock:
    requests_post.return_value.json.return_value = ci_catalog_response
    return requests_post


def test_get_all_component_versions_cached(
    tmp_path: pathlib.Path, requests_post: mock.Mock
) -> None:
    cache_path = tmp_path / "components" / "gitlab.com-project.json"
    cache_path.parent.mkdir()
    cache_path.write_text('[{"name": "v1.0.0","sha": "1"}]')

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions == [CatalogVersion("v1.0.0", "1")]

    requests_post.assert_not_called()


def test_get_all_component_versions_cache_corrupt(
    tmp_path: pathlib.Path, catalog_query: mock.Mock
) -> None:
    cache_path = tmp_path / "components" / "gitlab.com-project.json"
    cache_path.parent.mkdir()
    cache_path.write_text("not json")

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions

    catalog_query.assert_called()


def test_get_all_component_versions_out_of_date(
    tmp_path: pathlib.Path, catalog_query: mock.Mock
) -> None:
    cache_path = tmp_path / "components" / "gitlab.com-project.json"
    cache_path.parent.mkdir()
    cache_path.write_text('[{"name": "v1.0.0", "sha": "1"}]')

    try:
        os.utime(cache_path, (0, 0))
    except OSError:
        pytest.skip("Cannot set mtime")

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions == [
        CatalogVersion("v1.4.0", "b47a6c16e7e4f43e3bd573f029646464a20316b2")
    ]

    catalog_query.assert_called()


def test_get_all_component_versions(
    tmp_path: pathlib.Path, catalog_query: mock.Mock
) -> None:
    cache_path = tmp_path / "components" / "gitlab.com-project.json"
    assert not cache_path.exists()

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions == [
        CatalogVersion("v1.4.0", "b47a6c16e7e4f43e3bd573f029646464a20316b2")
    ]

    assert cache_path.exists()


def test_get_all_component_versions_authentication(
    tmp_path: pathlib.Path, catalog_query: mock.Mock, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "glpat-1234")

    cache_path = tmp_path / "components" / "gitlab.com-project.json"
    assert not cache_path.exists()

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions

    headers = catalog_query.call_args.kwargs["headers"]
    assert headers["Authorization"] == "Bearer glpat-1234"


def test_get_all_component_versions_pagination(
    tmp_path: pathlib.Path, requests_post: mock.Mock
) -> None:
    requests_post.return_value.json.side_effect = [
        ci_catalog_response_with_next_page,
        ci_catalog_response,
    ]

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert versions == [
        CatalogVersion("v1.3.0", "b47a6c16e7e4f43e3bd573f029646464a20316b2"),
        CatalogVersion("v1.4.0", "b47a6c16e7e4f43e3bd573f029646464a20316b2"),
    ]

    assert requests_post.call_count == 2
    assert requests_post.call_args.kwargs["json"]["variables"]["after"] == "MTM"


def test_get_all_component_versions_error(
    tmp_path: pathlib.Path, requests_post: mock.Mock
) -> None:
    requests_post.return_value.json.return_value = {"errors": [{"message": "test"}]}

    with pytest.raises(Exception, match="test"):
        get_all_component_versions(
            Arguments(cache_path=tmp_path),
            ComponentInclude("gitlab.com/project/test@~latest"),
        )


def test_get_all_component_versions_does_not_exist_error(
    tmp_path: pathlib.Path, requests_post: mock.Mock
) -> None:
    requests_post.return_value.json.return_value = {
        "errors": [
            {
                "message": "The resource that you are attempting to access does not "
                "exist or you don't have permission to perform this action."
            }
        ]
    }

    versions = get_all_component_versions(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert not versions


@pytest.fixture(name="get_command_output")
def mock_get_command_output() -> typing.Iterable[mock.Mock]:
    with mock.patch("trycicle.include.get_command_output") as m:
        yield m


def test_get_component_git_sha(
    tmp_path: pathlib.Path, get_command_output: mock.Mock
) -> None:
    get_command_output.return_value = (
        "b8918d1fbd54ad4dc0dae946496e8e0df5bfac37\trefs/tags/v0.0.1-alpha"
    )
    assert (
        get_component_git_sha(tmp_path, "v0.0.1-alpha")
        == "b8918d1fbd54ad4dc0dae946496e8e0df5bfac37"
    )


def test_get_component_git_sha_no_match(
    tmp_path: pathlib.Path, get_command_output: mock.Mock
) -> None:
    get_command_output.return_value = ""
    assert get_component_git_sha(tmp_path, "test") == "test"


def test_get_component_location(
    tmp_path: pathlib.Path,
    catalog_query: mock.Mock,
    run_command: mock.Mock,
    get_command_output: mock.Mock,
) -> None:
    repo_path = tmp_path / "components" / "gitlab.com-project-latest"

    location = get_component_location(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert location == repo_path
    assert location.exists()

    assert run_command.call_count == 3

    clone_command = run_command.call_args_list[0].args[0]
    assert clone_command[:2] == ["git", "clone"]
    assert clone_command[-2] == "git@gitlab.com:project.git"

    fetch_command = run_command.call_args_list[1].args[0]
    assert fetch_command[:2] == ["git", "fetch"]
    assert fetch_command[-1] == "b47a6c16e7e4f43e3bd573f029646464a20316b2"

    reset_command = run_command.call_args_list[2].args[0]
    assert reset_command[:2] == ["git", "reset"]
    assert reset_command[-1] == "b47a6c16e7e4f43e3bd573f029646464a20316b2"


def test_get_component_location_existing_repo(
    tmp_path: pathlib.Path,
    catalog_query: mock.Mock,
    run_command: mock.Mock,
    get_command_output: mock.Mock,
) -> None:
    repo_path = tmp_path / "components" / "gitlab.com-project-latest"
    repo_path.mkdir(parents=True)

    location = get_component_location(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@~latest"),
    )
    assert location == repo_path

    assert run_command.call_count == 2

    command = run_command.call_args_list[0].args[0]
    assert command[:2] != ["git", "clone"]


def test_get_component_location_version_not_in_catalog(
    tmp_path: pathlib.Path,
    catalog_query: mock.Mock,
    run_command: mock.Mock,
    get_command_output: mock.Mock,
) -> None:
    get_command_output.return_value = "sha1"

    repo_path = tmp_path / "components" / "gitlab.com-project-main"
    repo_path.mkdir(parents=True)

    location = get_component_location(
        Arguments(cache_path=tmp_path),
        ComponentInclude("gitlab.com/project/test@main"),
    )
    assert location == repo_path


def test_include_component() -> None:
    with mock.patch("trycicle.parser.get_component_location") as m:
        m.return_value = pathlib.Path("tests/examples/include/component")
        config = parse_example("component")

    assert "secret_detection" in config.jobs
    assert "included" in config.jobs
