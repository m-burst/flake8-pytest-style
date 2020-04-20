import sys

import pytest
from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.errors import PatchWithLambda
from flake8_pytest_style.visitors import PatchVisitor

HAS_POSITIONAL_ONLY_ARGS = sys.version_info >= (3, 8)

parametrize_code_template = pytest.mark.parametrize(
    'code_template',
    [
        "mocker.patch('module.name', {})",
        "module_mocker.patch('module.name', {})",
        "mocker.patch.object(obj, 'attr', {})",
        "module_mocker.patch.object(obj, 'attr', {})",
    ],
    ids=(
        'mocker.patch',
        'module_mocker.patch',
        'mocker.patch.object',
        'module_mocker.patch.object',
    ),
)


@parametrize_code_template
@pytest.mark.parametrize(
    'patch_with',
    [
        'not_lambda',
        'return_value=None',
        'lambda x, y: x',
        'lambda *args: args',
        'lambda **kwargs: kwargs',
        pytest.param(
            'lambda x, /, y: x',
            marks=[
                pytest.mark.skipif(
                    not HAS_POSITIONAL_ONLY_ARGS, reason=f'unsupported in {sys.version}'
                )
            ],
        ),
    ],
)
def test_ok(code_template, patch_with):
    code = code_template.format(patch_with)
    assert_not_error(PatchVisitor, code)


@parametrize_code_template
@pytest.mark.parametrize(
    'patch_with', ['lambda: None', 'lambda x, y: None', 'lambda *args, **kwargs: None']
)
def test_error(code_template, patch_with):
    code = code_template.format(patch_with)
    assert_error(PatchVisitor, code, PatchWithLambda)
