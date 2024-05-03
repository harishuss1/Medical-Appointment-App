from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.medical_room import MedicalRoom
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('medicalrooms', __name__, url_prefix='/medicalrooms/')


@bp.route('')
def get_medical_rooms():
    db = get_db()
    medicalrooms = db.get_medicalrooms()
    if medicalrooms is None or len(medicalrooms) == 0:
        abort(404)
    return render_template('medical_rooms.html', medicalrooms=medicalrooms)

@bp.route('/<string:room_number>/')
def get_medical_room(room_number):
    db = get_db()
    medical_room = db.get_medical_room_by_room_number(room_number)
    if medical_room is None:
        flash("Medical Room cannot be found", 'error')
        return redirect(url_for('medical_rooms.get_medical_rooms'))
    return render_template('specific_medical_room.html', medical_room=medical_room)
