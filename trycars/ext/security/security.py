from flask_security import Security, SQLAlchemySessionUserDatastore
from trycars.ext.database.database import db
from trycars.ext.database.models import User, Role
from flask_wtf import CSRFProtect


def init_app(app):
    with app.app_context():        
        CSRFProtect(app)
        user_datastore = SQLAlchemySessionUserDatastore(db, User, Role)
        app.security = Security(app, user_datastore)