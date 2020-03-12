from typing import List

import flake8
import pytest
from flake8.options.manager import OptionManager

from flake8_pytest_style.config import DEFAULT_CONFIG, Config, ParametrizeNamesType
from flake8_pytest_style.plugin import PytestStylePlugin


@pytest.fixture()
def option_manager() -> OptionManager:
    manager = OptionManager(prog='flake8', version=flake8.__version__)
    PytestStylePlugin.add_options(option_manager=manager)
    return manager


def parse_options(manager: OptionManager, args: List[str]) -> Config:
    namespace, remaining_args = manager.parse_args(args)
    return PytestStylePlugin.parse_options_to_config(manager, namespace, remaining_args)


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


def test_parse_parametrize_names_type(option_manager):
    config = parse_options(option_manager, ['--pytest-parametrize-names-type', 'csv'])
    assert config.parametrize_names_type is ParametrizeNamesType.CSV


def test_parse_parametrize_names_type_bad_value(option_manager):
    with pytest.raises(SystemExit):  # as raised by optparse
        parse_options(option_manager, ['--pytest-parametrize-names-type', 'str'])
