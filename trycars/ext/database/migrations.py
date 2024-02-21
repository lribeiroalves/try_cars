from flask_migrate import Migrate


migrate = Migrate()


def init_app(app, db):
    migrate.init_app(app, db, command='migration')