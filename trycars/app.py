from flask import Flask

from trycars.ext.configuration import configuration
from trycars.ext.database import database
from trycars.ext.commands import commands
from trycars.ext.mail_client import mail_client

from trycars.blueprints.development import bp_dev
from trycars.blueprints.homepage import bp_home


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)
    database.init_app(app)
    commands.init_app(app)
    mail_client.init_app(app)

    bp_dev.init_app(app)
    bp_home.init_app(app)

    return app