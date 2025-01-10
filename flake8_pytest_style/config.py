from enum import Enum
from typing import Any, List, NamedTuple, Type


def enum_choices(enum: Type[Enum]) -> List[Any]:
    return [member.value for member in enum]


class ParametrizeNamesType(Enum):
    CSV = 'csv'
    TUPLE = 'tuple'
    LIST = 'list'


class ParametrizeValuesType(Enum):
    TUPLE = 'tuple'
    LIST = 'list'


class ParametrizeValuesRowType(Enum):
    TUPLE = 'tuple'
    LIST = 'list'


class Config(NamedTuple):
    fixture_parentheses: bool
    raises_require_match_for: List[str]
    warns_require_match_for: List[str]
    parametrize_names_type: ParametrizeNamesType
    parametrize_values_type: ParametrizeValuesType
    parametrize_values_row_type: ParametrizeValuesRowType
    mark_parentheses: bool


DEFAULT_CONFIG = Config(
    fixture_parentheses=False,
    raises_require_match_for=[
        'BaseException',
        'Exception',
        'ValueError',
        'IOError',
        'OSError',
        'EnvironmentError',
        'socket.error',
    ],
    warns_require_match_for=['Warning', 'UserWarning', 'DeprecationWarning'],
    parametrize_names_type=ParametrizeNamesType.TUPLE,
    parametrize_values_type=ParametrizeValuesType.LIST,
    parametrize_values_row_type=ParametrizeValuesRowType.TUPLE,
    mark_parentheses=False,
)
