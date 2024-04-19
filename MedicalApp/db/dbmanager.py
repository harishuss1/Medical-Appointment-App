import os
import click
from flask import current_app, g
from .db import Database
from .fake_db import FakeDB


def get_db():
    testing = current_app.config['TESTING']
    if testing:
        if 'db' not in g:
            g.db = FakeDB()
    else:
        if 'db' not in g:
            g.db = Database()
    return g.db


def close_db(_):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    file_path = os.path.join(current_app.root_path, 'remove.sql')
    db.run_file(file_path)

    file_path = os.path.join(current_app.root_path, 'setup.sql')
    db.run_file(file_path)

    file_path = os.path.join(current_app.root_path, 'users.sql')
    db.run_file(file_path)


@click.command('init-db')
def init_db_command():
    click.echo('Setting up database')
    init_db()