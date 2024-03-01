import os
from flask import Flask

from trycars.ext.configuration import configuration


def minimal_app(**config):
    app = Flask(__name__)
    configuration.init_app(app, **config)

    return app


def create_app(**config):
    app = minimal_app(**config)
    if app.config['TESTING']:
        os.environ['FLASK_DEBUG'] = 'False'
        app.config['DEBUG'] = False
    configuration.load_extensions(app)

    return app