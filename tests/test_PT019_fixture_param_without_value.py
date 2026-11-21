import pytest
from flake8_plugin_utils.utils import assert_error, assert_not_error

from flake8_pytest_style.errors import FixtureParamWithoutValue
from flake8_pytest_style.visitors import TFunctionsVisitor


def test_ok_good_param_name():
    code = """
        def test_xxx(fixture):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_non_test_function():
    code = """
        def xxx(_param):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_error_arg():
    code = """
        def test_xxx(_fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


def test_error_kwonly():
    code = """
        def test_xxx(*, _fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


def test_ok_class_patch_decorators():
    code = """
        @patch.object(Config, 'get_first', return_value=None)
        @patch('src.app.config.controllers.db')
        class TestConfig:
            def test_config(self, _mock_db, _get_config):
                pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("namespace", ["", "mock.", "unittest.mock."])
@pytest.mark.parametrize(
    "patch_call", ["patch('module.name')", "patch.object(obj, 'attr')"]
)
@pytest.mark.parametrize("function_prefix", ["def", "async def"])
def test_ok_function_patch_decorator(namespace, patch_call, function_prefix):
    code = f"""
        @{namespace}{patch_call}
        {function_prefix} test_xxx(_mock):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize(
    "default", ["DEFAULT", "mock.DEFAULT", "unittest.mock.DEFAULT"]
)
@pytest.mark.parametrize(
    "patch_call",
    [
        "patch('module.name', {})",
        "patch('module.name', new={})",
        "patch.object(obj, 'attr', {})",
        "patch.object(obj, 'attr', new={})",
    ],
)
def test_ok_explicit_default(default, patch_call):
    code = f"""
        @{patch_call.format(default)}
        def test_xxx(_mock):
            pass
    """
    assert_not_error(TFunctionsVisitor, code)


def test_ok_class_and_method_patches():
    code = """
        @mock.patch('module.first')
        class TestConfig:
            @unittest.mock.patch.object(obj, 'second', autospec=True)
            async def test_config(self, _first, _second, fixture):
                pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize(
    ("signature", "decorators"),
    [
        ("self, _mock", ""),
        ("self, /, _mock", ""),
        ("cls, _mock", "@classmethod"),
        ("_mock", "@staticmethod"),
    ],
)
def test_ok_method_patch_decorator(signature, decorators):
    code = f"""
        class TestConfig:
            {decorators}
            @patch('module.name')
            def test_config({signature}):
                pass
    """
    assert_not_error(TFunctionsVisitor, code)


@pytest.mark.parametrize("signature", ["_mock, _fixture", "_mock, *, _fixture"])
def test_error_fixture_after_mock(signature):
    code = f"""
        @patch('module.name')
        def test_xxx({signature}):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


@pytest.mark.parametrize(
    "patch_call",
    [
        "patch('module.name', None)",
        "patch('module.name', new=None)",
        "patch.object(obj, 'attr', replacement)",
        "patch.object(obj, 'attr', new=replacement)",
        "patch.dict('module.mapping', {})",
        "unrelated.patch('module.name')",
        "patch(*args)",
        "patch('module.name', **kwargs)",
        "other_decorator",
    ],
)
def test_error_decorator_without_known_mock_argument(patch_call):
    code = f"""
        @{patch_call}
        def test_xxx(_fixture):
            pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


def test_error_class_fixture_after_mock():
    code = """
        @patch('module.first')
        class TestConfig:
            @patch.object(obj, 'second', new=None)
            def test_config(self, _mock, _fixture):
                pass
    """
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")


@pytest.mark.parametrize(
    "code",
    [
        """
            @patch('module.name')
            class TestPatched:
                def helper(self):
                    def test_nested(_fixture):
                        pass
        """,
        """
            @patch('module.name')
            class TestPatched:
                class TestNested:
                    def test_xxx(self, _fixture):
                        pass
        """,
        """
            @patch('module.name')
            class TestPatched:
                def test_xxx(self, _mock):
                    pass

            def test_unpatched(_fixture):
                pass
        """,
        """
            @patch('module.name')
            class TestPatched:
                def helper(self):
                    pass

                def test_xxx(self, _mock, _fixture):
                    pass
        """,
    ],
)
def test_error_class_patches_do_not_leak_between_scopes(code):
    assert_error(TFunctionsVisitor, code, FixtureParamWithoutValue, name="_fixture")
