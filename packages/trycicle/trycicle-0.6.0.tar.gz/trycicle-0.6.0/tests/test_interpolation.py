from unittest import mock

import pytest
import yaml

from trycicle.interpolation import Context, interpolate
from trycicle.variables import Variables


def test_interpolate() -> None:
    document = yaml.safe_load("""\
scan-website:
  image: test
  stage: $[[ inputs.job-stage ]]
  script: ./scan-website $[[ inputs.environment ]]
""")
    ctx = Context(
        inputs={"job-stage": "test", "environment": "production"},
        variables=Variables({}),
    )
    value = interpolate(ctx, document)
    assert value == {
        "scan-website": {
            "image": "test",
            "stage": "test",
            "script": "./scan-website production",
        }
    }


def test_interpolate_types() -> None:
    document = yaml.safe_load("""\
test_job:
  allow_failure: $[[ inputs.boolean_input ]]
  needs: $[[ inputs.array_input ]]
  parallel: $[[ inputs.number_input ]]
  script: $[[ inputs.string_input ]]
""")
    ctx = Context(
        inputs={
            "boolean_input": True,
            "array_input": ["one", "two"],
            "number_input": 1,
            "string_input": "test",
        },
        variables=Variables({}),
    )
    value = interpolate(ctx, document)
    assert value == {
        "test_job": {
            "allow_failure": True,
            "needs": ["one", "two"],
            "parallel": 1,
            "script": "test",
        }
    }


def test_interpolate_arrays_into_arrays() -> None:
    # Based on https://docs.gitlab.com/ee/ci/yaml/inputs.html#use-inputs-with-needs
    document = yaml.safe_load("""\
test_job:
  script: echo "this job has needs"
  needs:
    - $[[ inputs.first_needs ]]
    - $[[ inputs.second_needs ]]
""")
    ctx = Context(
        inputs={
            "first_needs": "job1",
            "second_needs": ["job2", "job3"],
        },
        variables=Variables({}),
    )
    value = interpolate(ctx, document)
    assert value == {
        "test_job": {
            "script": 'echo "this job has needs"',
            "needs": ["job1", "job2", "job3"],
        },
    }


def test_interpolate_functions() -> None:
    document = {"script": "echo $[[ inputs.test | expand_vars | truncate(5, 8) ]]"}
    ctx = Context(
        inputs={"test": "test $MY_VAR"},
        variables=Variables(
            {
                "MY_VAR": "my value",
            }
        ),
    )
    value = interpolate(ctx, document)
    assert value == {"script": "echo my value"}


@pytest.mark.parametrize(
    "document,expected",
    [
        ("$[[ inputs.int | expand_vars ]]", "can only be used with string inputs"),
        ("$[[ inputs.int | truncate(1, 1) ]]", "can only be used with string inputs"),
        ("$[[ test ]]", "unknown interpolation key"),
        ("$[[ inputs.x ]]", "unknown interpolation key"),
        ("$[[ inputs.int | f ]]", "no function matching"),
    ],
)
def test_interpolate_functions_invalid(document: str, expected: str) -> None:
    ctx = Context(
        inputs={"int": 1},
        variables=Variables({}),
    )
    with pytest.raises(ValueError, match=expected):
        interpolate(ctx, document)


def test_interpolate_caching() -> None:
    ctx = Context(
        inputs={"int": 1},
        variables=Variables({}),
    )

    with mock.patch("trycicle.interpolation.evaluate_access") as mock_access:
        mock_access.return_value = 42
        assert interpolate(ctx, "$[[ test ]] $[[ test ]]") == "42 42"

    assert mock_access.call_count == 1
