from flask_login import LoginManager

from trycars.ext.database.database import db
from trycars.ext.database.models import *


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return db.session.execute(db.select(User).filter_by(id=user_id)).scalar()


def init_app(app):
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'