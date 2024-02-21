from flask import Blueprint
from .views import register_views

bp_dev = Blueprint('development', __name__)


def init_app(app):
    register_views(bp_dev)
    app.register_blueprint(bp_dev)