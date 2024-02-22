from flask import Blueprint
from .views import register_views

bp_auth = Blueprint('auth', __name__, url_prefix='/auth/')


def init_app(app):
    register_views(bp_auth)
    app.register_blueprint(bp_auth)