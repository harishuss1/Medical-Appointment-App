import os 
from flask import Flask, render_template 
from .db.dbmanager import close_db, init_db_command 
from flask_login import LoginManager 
from MedicalApp.db.dbmanager import close_db, init_db_command, get_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    app.config.from_mapping(
        SECRET_KEY=os.environ['FLASK_SECRET'],
        ATTACHEMENTS=os.path.join(app.instance_path, "attachements")
    )

    app.config['IMAGES'] = os.path.join(app.instance_path, "IMAGES")

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['IMAGES'], exist_ok=True)

    os.makedirs(app.instance_path, exist_ok=True)
    os.makedirs(app.config['ATTACHEMENTS'], exist_ok=True)
    app.config['TESTING'] = False

    init_app(app)
    return app


def init_app(app):

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = get_db().get_user_by_id(user_id)
        return user
    
    #API logic:
    @login_manager.request_loader
    def request_loader(request): #special obj flask gives that represents everything in the request
        api_key = request.headers.get('Authorization')
        user = None
        if api_key:
            api_key = api_key.split(' ')[1]
            user = get_db().get_user_by_token(api_key)
        return user

    # REGISTER BLUEPRINTS HERE
    from .admin_view import admin_bp
    app.register_blueprint(admin_bp)

    from .auth_views import bp as login_bp
    app.register_blueprint(login_bp)

    from .doctor_view import bp as doctor_view_bp
    app.register_blueprint(doctor_view_bp)

    from .home_view import bp as home_bp
    app.register_blueprint(home_bp)

    from .patient_api import bp as patient_api_bp
    app.register_blueprint(patient_api_bp)

    from .doctor_api import bp as doctor_api_bp
    app.register_blueprint(doctor_api_bp)

    from .allergy_api import bp as allergy_bp
    app.register_blueprint(allergy_bp)

    from .appointments_views import bp as appointments_bp
    app.register_blueprint(appointments_bp)

    from .appointments_api import bp as appointments_api_bp
    app.register_blueprint(appointments_api_bp)

    from .note_views import bp as notes_bp
    app.register_blueprint(notes_bp)
    
    from .note_api import bp as note_bp
    app.register_blueprint(note_bp)

    from .patients_views import bp as patient_bp
    app.register_blueprint(patient_bp)

    from .user_views import bp as user_bp
    app.register_blueprint(user_bp)

    from .medical_rooms_view import bp as medical_rooms_bp
    app.register_blueprint(medical_rooms_bp)

    from .medical_room_api import bp as room_bp
    app.register_blueprint(room_bp)

    app.teardown_appcontext(close_db)

    app.cli.add_command(init_db_command)
