import pathlib
import typing


def rewrite_pattern(pattern: str) -> str:
    parts = pattern.split("/")
    last = len(parts) - 1
    for i, part in enumerate(parts):
        # pathlib interprets ** as any number of directories, including zero
        if part == "**" and i != last:
            parts[i] = "*/**"
        elif part != "**" and "**" in part:
            parts[i] = f"**/{part.replace('**','*')}"
    return "/".join(parts)


def glob(base: pathlib.Path, pattern: str) -> typing.Iterable[pathlib.Path]:
    if "*" in pattern or "?" in pattern or "[" in pattern:
        return base.glob(rewrite_pattern(pattern))
    else:
        return [base / pattern]
