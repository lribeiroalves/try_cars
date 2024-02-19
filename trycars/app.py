from flask import Flask

from trycars.ext.configuration import configuration
from trycars.ext.database import database
from trycars.ext.commands import commands

from trycars.blueprints.webui import webui


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    database.init_app(app)
    commands.init_app(app)
    webui.init_app(app)

    return app