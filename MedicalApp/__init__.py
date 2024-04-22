import os
from flask import Flask, render_template
from MedicalApp.db.dbmanager import close_db, init_db_command


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET']
    )
    app.config['TESTING'] = False

    init_app(app)
    return app


def init_app(app):
    # REGISTER BLUEPRINTS HERE
    from .appointments_views import bp as appointments_bp
    app.register_blueprint(appointments_bp)

    app.teardown_appcontext(close_db)

    app.cli.add_command(init_db_command)
