import pytest
from trycars.app import create_app, minimal_app
from trycars.ext.database.database import db
from trycars.ext.commands.commands import init_db, drop_db, populate_db


@pytest.fixture(scope='session')
def min_app():
    """Minimal instance of Main flask app"""
    return minimal_app(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.fixture(scope='session')
def app():
    """Instance of Main flask app with access to the database"""
    app =  create_app(FORCE_ENV_FOR_DYNACONF="testing")
    with app.app_context():
        init_db()
        populate_db()
        yield app
        drop_db()


@pytest.fixture(scope='session')
def populate(app):
    """Populates the database for testing"""
    with app.app_context():
        populate_db()
        return
    