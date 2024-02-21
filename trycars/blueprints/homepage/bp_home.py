from flask import Blueprint
from .views import register_views

bp_home = Blueprint('homepage', __name__)


def init_app(app):
    register_views(bp_home)
    app.register_blueprint(bp_home)