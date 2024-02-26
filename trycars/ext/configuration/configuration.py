from importlib import import_module
from dynaconf import Dynaconf, FlaskDynaconf


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)


def load_extensions(app):
    for ext in app.config.EXTENSIONS:
        module_name, factory = ext.split(':')
        extension = import_module(module_name)
        getattr(extension, factory)(app)


def init_app(app, **config):
    FlaskDynaconf(app, **config)