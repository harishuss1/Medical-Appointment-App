from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.forms import AddMedicalRoom
from MedicalApp.medical_room import MedicalRoom
from .db.dbmanager import get_db

bp = Blueprint('medical_rooms', __name__, url_prefix='/medicalrooms/')

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('')
@login_required
def get_medical_rooms():
    try:
        db = get_db()
        medicalrooms = db.get_medical_rooms()
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('home.index')
    if medicalrooms is None or len(medicalrooms) == 0:
        abort(404)
    return render_template('medical_rooms.html', medicalrooms=medicalrooms)

@bp.route('/<string:room_number>/')
@login_required
def get_medical_room(room_number):
    try:
        db = get_db()
        medical_room = db.get_medical_room_by_room_number(room_number)
        if medical_room is None:
            flash("Medical Room cannot be found", 'error')
            return redirect(url_for('medical_rooms.get_medical_rooms'))
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect(url_for('home.index'))
    return render_template('specific_medical_room.html', medical_room=medical_room)

@bp.route('/add/', methods=['GET', 'POST'])
@login_required
@doctor_access
def add_medical_room():
    form = AddMedicalRoom()
    if request.method == 'POST' and form.validate_on_submit():
        room_number = form.room.data
        description = form.description.data
        try:
            room = get_db().get_patients_by_id(room_number)
            if room is not None:
                flash("this room already exists")
                form = AddMedicalRoom()
                return redirect(render_template('add_room.html', form=form))
            get_db().add_medical_room(room_number, description)
            return redirect(url_for('medical_room.get_medical_room', room_number=room_number))
        except DatabaseError as e:
            flash("something went wrong with the database")
        except ValueError as e:
            flash("Incorrect values were passed")
    return render_template('add_room.html', form=form)
