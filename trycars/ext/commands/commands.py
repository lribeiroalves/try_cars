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
    roles = [
        Role(name = 'admin', description='Admin User Privileges'),
        Role(name = 'user', description='Simple User'),
    ]
    db.session.add_all(roles)
    db.session.commit()
    
    data = [
        User(id = 1, email = 'lucasribeiroalves@live.com', username = 'lribeiro', password = '1234', active = True, fs_uniquifier = '0123456789', roles=roles[0]),
        User(id = 2, email = 'lu_ks_2009@hotmail.com', username = 'lucasralves', password = '1234', active = True, fs_uniquifier = '9876543210', roles=roles[1]),
    ]
    db.session.add_all(data)
    db.session.commit()


def roles_db():
    roles = [
        Role(name = 'admin', description='Admin User Privileges'),
        Role(name = 'user', description='Simple User'),
    ]
    db.session.add_all(roles)
    db.session.commit()

    click.echo('Roles Created')



def init_app(app):
    for command in [init_db, drop_db, populate_db, roles_db]:
        app.cli.add_command(app.cli.command()(command))
