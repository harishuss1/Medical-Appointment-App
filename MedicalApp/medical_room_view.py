from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.medical_room import MedicalRoom
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('medicalrooms', __name__, url_prefix='/medicalrooms/')


@bp.route('')
# @login_required
def get_medical_rooms():
    db = get_db()
    medicalrooms = db.get_medicalrooms()
    if medicalrooms is None or len(medicalrooms) == 0:
        abort(404)
    return render_template('medicalRooms.html',medicalrooms=medicalrooms)


'''
    form = AppointmentForm()
    if request.method == "POST" and form.validate_on_submit():
        id = form.id.data
        patient_id = form.patient_id.data
        doctor_id = form.doctor_id.data
        appointment_id = form.province.data
        status = form.status.data
        location = form.location.data
        description = form.description.data
        new_appointment = Appointments(
            id, patient_id, doctor_id, appointment_id, status, location, description)

        # checks if theres any existing appointment in the appointments list and it will check if it matches with
        # the new appointment, if match then it flashed that it already exist and
        # will not take the new appointment
        if any(
            appointment.id == new_appointment.id and
            appointment.patient_id == new_appointment.patient_id and
            appointment.doctor_id == new_appointment.doctor_id
            for appointment in appointments
        ):
            flash("Appointment already exists", "error")
        else:
            new_appointment = Appointments(
                id, patient_id, doctor_id, appointment_id, status, location, description)
            db.add_appointment(new_appointment)
            flash("Appointement added to the List of Appointments")

            return redirect(
                url_for('appointments.get_appointment', id=new_appointment.id))
    '''


@bp.route('/<string:room_number>/')
# @login_required
def get_medical_room(room_number):
    db = get_db()
    medical_room = db.get_room_number_by_room_name(room_number)
    if medical_room is None:
        flash("Medical Room cannot be found", 'error')
        return redirect(url_for('medical_rooms.get_medical_rooms'))
    return render_template('specific_medical_room.html', medical_room=medical_room)