from flask import Flask
from .dbmanager import close_db, init_db_command
import os


def create_app(test_config=False):
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = os.environ['FLASK_SECRET']
    app.config['TESTING'] = test_config
    init_app(app)
    return app


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

    return app
