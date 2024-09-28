import dataclasses
import pathlib
import typing
from functools import cached_property

import platformdirs

from .variables import Variables, get_predefined_variables

DebugEnabled = typing.Literal["true", "false", "immediate"]


def get_cache_path() -> pathlib.Path:
    return pathlib.Path(platformdirs.user_cache_dir("trycicle"))


@dataclasses.dataclass
class Arguments:
    original_dir: pathlib.Path = pathlib.Path()
    service_logs: bool = False
    debugger: DebugEnabled = "false"
    cache_path: pathlib.Path = dataclasses.field(default_factory=get_cache_path)
    clean_copy: bool = False

    cache_directory: dataclasses.InitVar[pathlib.Path | None] = None

    def __post_init__(self, cache_directory: pathlib.Path | None) -> None:
        self.original_dir = self.original_dir.absolute()
        if cache_directory is not None:
            self.cache_path = cache_directory

    @property
    def interactive(self) -> bool:
        return self.debugger != "false"

    @cached_property
    def variables(self) -> Variables:
        return get_predefined_variables(self.original_dir)

    def without_variables(self) -> typing.Self:
        copy = dataclasses.replace(self)
        copy.__dict__["variables"] = Variables({})
        return copy
