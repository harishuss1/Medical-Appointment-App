from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.appointments import Appointments
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')

def patient_access(func):
    def wrapper():
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func()
    wrapper.__name__ = func.__name__
    return wrapper

def doctor_access(func):
    def wrapper():
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func()
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/appointments/')
@login_required
@patient_access
def view_appointments():
    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_appointments.html', appointments=appointments)

@bp.route('', methods=['GET', 'POST'])
@login_required
@patient_access
def get_appointments():
    db = get_db()
    appointments = db.get_appointments()
    if appointments is None or len(appointments) == 0:
        abort(404)

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

    return render_template('appointments.html', form=form)


@bp.route('/<int:id>/')
@login_required
@patient_access
def get_appointment(id):
    db = get_db()
    appointment = db.get_appointment_id(id)
    if appointment is None:
        flash("Appointment cannot be found", 'error')
        return redirect(url_for('appointments.get_appointments'))
    return render_template('specific_appointment.html', appointment=appointment)


@bp.route('/confirmed/<string:user_type>/')
@login_required
@patient_access
def confirmed_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('hone.index'))
    try:
        appointments = None
        if user_type == 'doctor':
            appointments = get_db().get_appointments_by_status_doctor(1, current_user.id)
        if user_type == 'patient':
            appointments = get_db().get_appointments_by_status_patient(1, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('confirmed_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/<string:user_type>/')
@login_required
@patient_access
def requested_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('hone.index'))
    try:
        appointments = None
        if user_type == 'doctor':
            appointments = get_db().get_appointments_by_status_doctor(0, current_user.id)
        if user_type == 'patient':
            appointments = get_db().get_appointments_by_status_patient(0, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('requested_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))

# CHANGE!!!
@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
@login_required
@doctor_access
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
