from flake8_plugin_utils import assert_error, assert_not_error

from flake8_pytest_style.config import DEFAULT_CONFIG
from flake8_pytest_style.errors import FixtureFinalizerCallback
from flake8_pytest_style.visitors import FixturesVisitor


def test_ok_return():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            return 0
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_yield():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            resource = acquire_resource()
            yield resource
            resource.release()
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_other_request():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture():
            request = get_request()
            request.addfinalizer(finalizer)
            return request
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_other_function():
    # factory fixtures are a tricky use-case where addfinalizer cannot be replaced
    # inspired by tls_http_server fixture in cherrypy/cheroot
    code = """
        import functools
        import pytest

        def create_resource(arg, request):
            resource = Resource(arg)
            request.addfinalizer(resource.release)
            return resource

        @pytest.fixture()
        def resource_factory(request):
            return functools.partial(create_resource, request=request)
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_ok_nested_function():
    # https://github.com/m-burst/flake8-pytest-style/issues/46
    code = """
        import pytest

        @pytest.fixture()
        def resource_factory(request):
            def create_resource(arg) -> Resource:
                resource = Resource(arg)
                request.addfinalizer(resource.release)
                return resource
            return create_resource
    """
    assert_not_error(FixturesVisitor, code, config=DEFAULT_CONFIG)


def test_error_return():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture(request):
            resource = acquire_resource()
            request.addfinalizer(resource.release)
            return resource
    """
    assert_error(FixturesVisitor, code, FixtureFinalizerCallback, config=DEFAULT_CONFIG)


def test_error_yield():
    code = """
        import pytest

        @pytest.fixture()
        def my_fixture(request):
            resource = acquire_resource()
            request.addfinalizer(resource.release)
            yield resource
    """
    assert_error(FixturesVisitor, code, FixtureFinalizerCallback, config=DEFAULT_CONFIG)
