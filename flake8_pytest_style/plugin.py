import argparse
from typing import List

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin

from .config import DEFAULT_CONFIG, Config
from .visitors import (
    FixturesVisitor,
    ImportsVisitor,
    ParametrizeVisitor,
    PatchVisitor,
    RaisesVisitor,
    UnittestAssertionVisitor,
)

__version__ = '0.5.0'


class PytestStylePlugin(Plugin[Config]):
    name = 'flake8-pytest-style'
    version = __version__
    visitors = [
        FixturesVisitor,
        ImportsVisitor,
        PatchVisitor,
        ParametrizeVisitor,
        RaisesVisitor,
        UnittestAssertionVisitor,
    ]

    @classmethod
    def add_options(cls, option_manager: OptionManager) -> None:
        option_manager.add_option(
            '--pytest-fixture-no-parentheses',
            action='store_true',
            parse_from_config=True,
            default=not DEFAULT_CONFIG.fixture_parentheses,
            help='Omit parentheses for @pytest.fixture decorators'
            ' without parameters. (Default: %default)',
        )
        option_manager.add_option(
            '--pytest-raises-require-match-for',
            comma_separated_list=True,
            parse_from_config=True,
            default=DEFAULT_CONFIG.raises_require_match_for,
            help='List of exceptions for which flake8-pytest-style requires'
            ' a match= argument in pytest.raises(). (Default: %default)',
        )

    @classmethod
    def parse_options_to_config(  # pylint: disable=unused-argument
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(
            fixture_parentheses=not options.pytest_fixture_no_parentheses,
            raises_require_match_for=options.pytest_raises_require_match_for,
        )
