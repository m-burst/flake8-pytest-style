from typing import List, NamedTuple


class Config(NamedTuple):
    fixture_parentheses: bool
    raises_require_match_for: List[str]


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
)
