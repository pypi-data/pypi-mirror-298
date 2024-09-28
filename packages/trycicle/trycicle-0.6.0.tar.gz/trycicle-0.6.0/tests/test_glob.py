import pathlib

import pytest

from trycicle.glob import glob, rewrite_pattern


@pytest.mark.parametrize(
    "pattern,expected",
    [
        ("*.txt", "*.txt"),
        ("**", "**"),
        ("**/*.txt", "*/**/*.txt"),
        ("**.txt", "**/*.txt"),
    ],
)
def test_rewrite_pattern(pattern: str, expected: str) -> None:
    assert rewrite_pattern(pattern) == expected


@pytest.mark.parametrize(
    "pattern,expected",
    [
        pytest.param(
            "*.yml",
            [".gitlab-ci.yml", "one.yml"],
            id="glob",
        ),
        pytest.param(
            "**.yml",
            [".gitlab-ci.yml", "one.yml", "a/a.yml", "a/b/b.yml", "a/b/c/c.yml"],
            id="all",
        ),
        pytest.param(
            "**",
            [".", "a", "a/b", "a/b/c"],
            id="directories",
        ),
        pytest.param(
            "**/*.yml",
            ["a/a.yml", "a/b/b.yml", "a/b/c/c.yml"],
            id="subdir",
        ),
        pytest.param("foo", ["foo"], id="literal"),
    ],
)
def test_glob(pattern: str, expected: list[str]) -> None:
    path = pathlib.Path("tests/examples/include/wildcards")
    matches = sorted(
        (str(match.relative_to(path)) for match in glob(path, pattern)),
        key=lambda m: (m.count("/"), m),
    )
    assert matches == expected
