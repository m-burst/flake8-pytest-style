from enum import Enum
from typing import List, NamedTuple


class ParametrizeNamesType(Enum):
    CSV = 'csv'
    TUPLE = 'tuple'
    LIST = 'list'


class Config(NamedTuple):
    fixture_parentheses: bool
    raises_require_match_for: List[str]
    parametrize_names_type: ParametrizeNamesType


DEFAULT_CONFIG = Config(
    fixture_parentheses=True,
    raises_require_match_for=[
        'BaseException',
        'Exception',
        'ValueError',
        'IOError',
        'OSError',
        'EnvironmentError',
        'socket.error',
    ],
    parametrize_names_type=ParametrizeNamesType.TUPLE,
)
