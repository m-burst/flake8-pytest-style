from typing import List, NamedTuple


class Config(NamedTuple):
    raises_require_match_for: List[str]


DEFAULT_CONFIG = Config(
    raises_require_match_for=[
        'BaseException',
        'Exception',
        'ValueError',
        'IOError',
        'OSError',
        'EnvironmentError',
        'socket.error',
    ]
)
