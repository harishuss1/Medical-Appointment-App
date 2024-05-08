from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.medical_room import MedicalRoom
from .db.dbmanager import get_db

bp = Blueprint('medical_rooms', __name__, url_prefix='/medicalrooms/')


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
