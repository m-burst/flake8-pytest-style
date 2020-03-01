import typing
from typing import NamedTuple


class Config(NamedTuple):
    no_bare_raises_exceptions: typing.List[str]
