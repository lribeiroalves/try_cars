import click
from trycars.ext.database.database import db
from trycars.ext.database.models import *


def init_db():
    """Creates the database"""
    db.create_all()
    click.echo('Initialized the database')


def drop_db():
    """Drop the entire database"""
    db.drop_all()
    click.echo("Droped the entire database")

def populate_db():
    data = [
        User(id = 1, email = 'lucasribeiroalves@live.com', username = 'lribeiro', password = '1234', active = True, fs_uniquifier = '0123456789', roles=Role(name = 'admin', description='Admin User Privileges')),
    ]
    db.session.add_all(data)
    db.session.commit()


def init_app(app):
    for command in [init_db, drop_db, populate_db]:
        app.cli.add_command(app.cli.command()(command))
