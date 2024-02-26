import pytest
from trycars.app import create_app, minimal_app


@pytest.fixture(scope='session')
def min_app():
    """Minimal instance of Main flask app"""
    return minimal_app(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope='session')
def app():
    """Minimal instance of Main flask app"""
    return create_app(FORCE_ENV_FOR_DYNACONF="testing")