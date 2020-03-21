import argparse
from typing import List

from flake8.options.manager import OptionManager
from flake8_plugin_utils import Plugin

from .config import (
    DEFAULT_CONFIG,
    Config,
    ParametrizeNamesType,
    ParametrizeValuesRowType,
    ParametrizeValuesType,
    enum_choices,
)
from .visitors import (
    FixturesVisitor,
    ImportsVisitor,
    ParametrizeVisitor,
    PatchVisitor,
    RaisesVisitor,
    UnittestAssertionVisitor,
)

__version__ = '0.6.0'


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
        option_manager.add_option(
            '--pytest-parametrize-names-type',
            choices=enum_choices(ParametrizeNamesType),
            parse_from_config=True,
            default=DEFAULT_CONFIG.parametrize_names_type.value,
            help='Preferred type for multiple parameter names in'
            ' @pytest.mark.parametrize. (Default: %default)',
        )
        option_manager.add_option(
            '--pytest-parametrize-values-type',
            choices=enum_choices(ParametrizeValuesType),
            parse_from_config=True,
            default=DEFAULT_CONFIG.parametrize_values_type.value,
            help='Preferred type for values in @pytest.mark.parametrize.'
            ' (Default: %default)',
        )
        option_manager.add_option(
            '--pytest-parametrize-values-row-type',
            choices=enum_choices(ParametrizeValuesRowType),
            parse_from_config=True,
            default=DEFAULT_CONFIG.parametrize_values_row_type.value,
            help='Preferred type for each row in @pytest.mark.parametrize'
            ' in case of multiple parameters. (Default: %default)',
        )

    @classmethod
    def parse_options_to_config(  # pylint: disable=unused-argument
        cls, option_manager: OptionManager, options: argparse.Namespace, args: List[str]
    ) -> Config:
        return Config(
            fixture_parentheses=not options.pytest_fixture_no_parentheses,
            raises_require_match_for=options.pytest_raises_require_match_for,
            parametrize_names_type=ParametrizeNamesType(
                options.pytest_parametrize_names_type
            ),
            parametrize_values_type=ParametrizeValuesType(
                options.pytest_parametrize_values_type
            ),
            parametrize_values_row_type=ParametrizeValuesRowType(
                options.pytest_parametrize_values_row_type
            ),
        )
