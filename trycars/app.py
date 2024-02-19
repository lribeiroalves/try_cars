from flask import Flask

from trycars.ext.configuration import configuration


def create_app():
    app = Flask(__name__)
    configuration.init_app(app)

    return app