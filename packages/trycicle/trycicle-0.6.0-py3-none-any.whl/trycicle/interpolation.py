import dataclasses
import re
import typing

from .variables import Variables


@dataclasses.dataclass
class Context:
    inputs: dict[str, typing.Any]
    variables: Variables
    blocks: dict[str, typing.Any] = dataclasses.field(default_factory=dict)


@dataclasses.dataclass
class Function:
    pattern: re.Pattern[str]
    function: typing.Callable[[Context, typing.Any, dict[str, str]], typing.Any]


def expand_vars(ctx: Context, value: typing.Any, args: dict[str, str]) -> str:
    if not isinstance(value, str):
        raise ValueError("expand_vars can only be used with string inputs")
    return ctx.variables.replace(value)


def truncate(ctx: Context, value: typing.Any, args: dict[str, str]) -> str:
    if not isinstance(value, str):
        raise ValueError("truncate can only be used with string inputs")
    offset = int(args["offset"])
    length = int(args["length"])
    return value[offset:][:length]


functions = [
    Function(
        re.compile(r"expand_vars"),
        expand_vars,
    ),
    Function(
        re.compile(r"truncate\(\s*(?P<offset>\d+)\s*,\s*(?P<length>\d+)\s*\)"),
        truncate,
    ),
]


def evaluate_access(ctx: Context, access: str) -> typing.Any:
    [inputs, *parts] = access.split(".")
    if inputs != "inputs":
        raise ValueError(f"unknown interpolation key `{inputs}`")
    value = ctx.inputs
    for part in parts:
        assert isinstance(value, dict)
        if part not in value:
            raise ValueError(f"unknown interpolation key `{part}`")
        value = value[part]
    return value


def evaluate_function(ctx: Context, value: typing.Any, expression: str) -> typing.Any:
    for f in functions:
        if match := f.pattern.match(expression):
            return f.function(ctx, value, match.groupdict())
    raise ValueError(f"no function matching `{expression}`")


def evaluate_block(ctx: Context, block: str) -> typing.Any:
    if block not in ctx.blocks:
        [access, *pipeline] = [part.strip() for part in block.split("|")]
        value = evaluate_access(ctx, access)
        for part in pipeline:
            value = evaluate_function(ctx, value, part)
        ctx.blocks[block] = value
    return ctx.blocks[block]


def interpolate(ctx: Context, value: typing.Any) -> typing.Any:
    if isinstance(value, dict):
        return {interpolate(ctx, k): interpolate(ctx, v) for k, v in value.items()}

    if isinstance(value, list):
        new_value = []
        for item in value:
            new_item = interpolate(ctx, item)
            if isinstance(item, str) and isinstance(new_item, list):
                new_value.extend(new_item)
            else:
                new_value.append(new_item)
        return new_value

    if isinstance(value, str) and "$[[" in value:
        blocks = list(re.finditer(r"\$\[\[\s*(\S.*?\S)\s*]]", value))
        # If there is only one block, and it spans the entire node, replace it.
        if len(blocks) == 1 and blocks[0].group(0) == value:
            return evaluate_block(ctx, blocks[0].group(1))

        # Otherwise, interpolate each block into the value.
        for block in blocks:
            value = value.replace(
                block.group(0), str(evaluate_block(ctx, block.group(1)))
            )

    return value
