from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import trycars.ext.database.migrations as migrations


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def init_app(app):
    db.init_app(app)
    migrations.init_app(app, db)
    app.teardown_appcontext(lambda exc: db.session.close())