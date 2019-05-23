import pytest

from flake8_pytest_style._vendor.flake8_plugin_utils import (
    assert_error,
    assert_not_error,
)
from flake8_pytest_style.errors import PatchWithLambda
from flake8_pytest_style.visitors import PytestStyleVisitor

parametrize_code_template = pytest.mark.parametrize(
    'code_template',
    ["mocker.patch('module.name', {})", "mocker.patch.object(obj, 'attr', {})"],
    ids=('patch', 'patch.object'),
)


@parametrize_code_template
@pytest.mark.parametrize(
    'patch_with', ['not_lambda', 'return_value=None', 'lambda x, y: x']
)
def test_ok(code_template, patch_with):
    code = code_template.format(patch_with)
    assert_not_error(PytestStyleVisitor, code)


@parametrize_code_template
@pytest.mark.parametrize('patch_with', ['lambda: None', 'lambda x, y: None'])
def test_error(code_template, patch_with):
    code = code_template.format(patch_with)
    assert_error(PytestStyleVisitor, code, PatchWithLambda)
