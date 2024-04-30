from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.appointments import Appointments
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')


from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from MedicalApp.appointments import Appointments
from MedicalApp.forms import AppointmentForm
from MedicalApp.db import db, dbmanager

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')


@bp.route('', methods=['GET', 'POST'])
# @login_required
def get_appointments():
    db = dbmanager.get_db()
    appointments = db.get_appointments()
    if appointments is None or len(appointments) == 0:
        abort(404)

    form = AppointmentForm()
    if request.method == "POST" and form.validate_on_submit():
        id = form.id.data
        patient = db.get_user_by_id(form.patient_id.data)
        doctor = db.get_user_by_id(form.doctor_id.data)
        appointment_id = form.province.data
        status = form.status.data
        location = form.location.data
        description = form.description.data
        new_appointment = Appointments(
            id, patient, doctor, appointment_id, status, location, description)

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
                id, patient, doctor, appointment_id, status, location, description)
            db.add_appointment(new_appointment)
            flash("Appointement added to the List of Appointments")

            return redirect(
                url_for('appointments.get_appointment', id=new_appointment.id))

    return render_template('appointments.html', appointments=appointments, form=form)


@bp.route('/<int:id>/')
# @login_required
def get_appointment(id):
    db = dbmanager.get_db()
    appointment = db.get_appointment_by_id(id)
    if appointment is None:
        flash("Appointment cannot be found", 'error')
        return redirect(url_for('appointments.get_appointments'))
    return render_template('specific_appointment.html', appointment=appointment)


@bp.route('/confirmed/')
@login_required
def confirmed_appointments():
    try:
        appointments = None
        if current_user.access_level == 'STAFF':
            appointments = get_db().get_appointments_by_status_doctor(1, current_user.id)
        if current_user.access_level == 'PATIENT':
            appointments = get_db().get_appointments_by_status_patient(1, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('confirmed_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/')
@login_required
def requested_appointments():
    try:
        appointments = None
        if current_user.access_level == 'STAFF':
            appointments = get_db().get_appointments_by_status_doctor(0, current_user.id)
        if current_user.access_level == 'PATIENT':
            appointments = get_db().get_appointments_by_status_patient(0, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('requested_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
@login_required
def update_appointment(id):
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    form = AppointmentResponseForm()
    appointment = get_db().get_appointment_by_id(id)
    if request.method == 'POST' and form.validate_on_submit():
        status = form.select_confirmation.data
        try:
            get_db().update_appointment_status(id, status)
            flash("Appointment has been successfully updated")
            return redirect(url_for('doctor.requested_appointments'))
        except DatabaseError:
            flash("Something went wrong with the database")
            return redirect(url_for('doctor.requested_appointments'))

    if appointment is None:
        abort(404, "This address does not exist")
    return render_template('requested_appointment.html', appointment=appointment, form=form)
