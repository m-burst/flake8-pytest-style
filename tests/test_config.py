from typing import List

import flake8
import pytest
from flake8.options.manager import OptionManager

from flake8_pytest_style.config import (
    DEFAULT_CONFIG,
    Config,
    ParametrizeNamesType,
    ParametrizeValuesRowType,
    ParametrizeValuesType,
)
from flake8_pytest_style.plugin import PytestStylePlugin


@pytest.fixture
def option_manager() -> OptionManager:
    manager = OptionManager(
        version=flake8.__version__,
        plugin_versions='',  # Not necessary in tests
        parents=[],
        formatter_names=[],
    )
    PytestStylePlugin.add_options(option_manager=manager)
    return manager


def parse_options(manager: OptionManager, args: List[str]) -> Config:
    namespace = manager.parse_args(args)
    return PytestStylePlugin.parse_options_to_config(
        manager,
        namespace,
        # Not sure if this is semantically correct, but this is what flake8 passes
        # to plugin's parse_options
        namespace.filenames,
    )


def test_parse_default(option_manager):
    assert parse_options(option_manager, []) == DEFAULT_CONFIG


def test_parse_raises_require_match_for(option_manager):
    config = parse_options(
        option_manager, ['--pytest-raises-require-match-for', 'ValueError,TypeError']
    )
    assert config.raises_require_match_for == ['ValueError', 'TypeError']


def test_parse_fixture_parentheses(option_manager):
    config = parse_options(option_manager, ['--pytest-fixture-no-parentheses'])
    assert config.fixture_parentheses is False


@pytest.mark.parametrize('value', list(ParametrizeNamesType))
def test_parse_parametrize_names_type(option_manager, value):
    config = parse_options(
        option_manager, ['--pytest-parametrize-names-type', value.value]
    )
    assert config.parametrize_names_type is value


@pytest.mark.parametrize('value', list(ParametrizeValuesType))
def test_parse_parametrize_values_type(option_manager, value):
    config = parse_options(
        option_manager, ['--pytest-parametrize-values-type', value.value]
    )
    assert config.parametrize_values_type is value


@pytest.mark.parametrize('value', list(ParametrizeValuesRowType))
def test_parse_parametrize_values_row_type(option_manager, value):
    config = parse_options(
        option_manager, ['--pytest-parametrize-values-row-type', value.value]
    )
    assert config.parametrize_values_row_type is value


@pytest.mark.parametrize(
    'args',
    [
        ['--pytest-parametrize-names-type', 'str'],
        ['--pytest-parametrize-values-type', 'str'],
        ['--pytest-parametrize-values-row-type', 'str'],
    ],
)
def test_parse_invalid_enum_values(option_manager, args):
    with pytest.raises(SystemExit):  # as raised by optparse
        parse_options(option_manager, args)
