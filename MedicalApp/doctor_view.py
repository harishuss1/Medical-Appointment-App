from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import current_user, login_user, logout_user, login_required
from .forms import AppointmentResponseForm
from .db.db import Database

bp = Blueprint('doctor', __name__, url_prefix="/doctor/")


@bp.route('/')
@login_required
def dashboard():
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    return render_template("doctor.html")


@bp.route('/appointments/')
@login_required
def confirmed_appointments():
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    try:
        appointments = get_db().get_appointments_by_status(1, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_appointments.html', appointments=appointments, get_db=get_db, get_user_by_id=get_db().get_user_by_id)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/')
@login_required
def requested_appointments():
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    try:
        appointments = get_db().get_appointments_by_status(0, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_requests.html', appointments=appointments, get_db=get_db, get_user_by_id=get_db().get_user_by_id)
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
    return render_template('requested_appointment.html', appointment=appointment, form=form, get_db=get_db, get_user_by_id=get_db().get_user_by_id)


@bp.route('/patients/')
@login_required
def patients():
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    try:
        patients = get_db().get_patients_by_doctor(current_user.id)
        if patients is None or len(patients) == 0:
            flash("No patients are currently being supervised by you")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_patients.html', patients=patients)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/notes/<int:patient_id>')
@login_required
def notes(patient_id):
    if current_user.access_level != 'STAFF':
        return redirect(url_for('home.index'))
    try:
        patient = get_db().get_patients_by_id(patient_id)
        notes = get_db().get_notes_by_patient_id(patient_id, current_user.id)
        if notes is None or len(notes) == 0:
            flash("No notes are currently written for this patient")
            return redirect(url_for('doctor.dashboard'))
        if patient is None:
            flash("Patient does not exist")
            return redirect(url_for('doctor.dashboard'))
        return render_template('patient_notes.html', notes=notes, patient=patient)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))
