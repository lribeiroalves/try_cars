from flask import Blueprint
from .views import register_views

bp = Blueprint('webui', __name__)


def init_app(app):
    register_views(bp)
    app.register_blueprint(bp)