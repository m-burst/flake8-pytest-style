import argparse
from typing import List

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin

from .config import Config
from .visitors import PytestStyleVisitor

__version__ = '0.2.0'


class PytestStylePlugin(Plugin[Config]):
    name = 'flake8-pytest-style'
    version = __version__
    visitors = [PytestStyleVisitor]

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:  # pragma: no cover
        option_manager.add_option(
            '--pytest-raises-require-match-for',
            comma_separated_list=True,
            parse_from_config=True,
        )

    @classmethod
    def parse_options_to_config(  # pylint: disable=unused-argument
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:  # pragma: no cover
        return Config(raises_require_match_for=options.pytest_raises_require_match_for)
