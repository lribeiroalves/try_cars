from dynaconf import Dynaconf, FlaskDynaconf


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['settings.toml', '.secrets.toml'],
)


def init_app(app):
    FlaskDynaconf(app)