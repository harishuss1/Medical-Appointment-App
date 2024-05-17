from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from oracledb import DatabaseError
from MedicalApp.appointments import Appointments
from .forms import AppointmentForm, AppointmentResponseForm
from .db.dbmanager import get_db

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')


def patient_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/book/', methods=['GET', 'POST'])
@login_required
@patient_access
def book_appointment():
    form = AppointmentForm()
    form.set_patients()
    form.set_doctors()
    form.set_rooms()
    user = 'doctor'
    if current_user.access_level == 'PATIENT':
        if get_db().get_patients_by_id(current_user.id) is None:
            flash("Please update your patient details before booking an appointment")
            return redirect(url_for('patient.update_patient'))
        user = 'patient'
        form.patient.data = str(current_user.id)
        form.patient.render_kw = {'disabled' : ''} 
        form.location.data = '101'
        form.location.render_kw = {'disabled' : ''}
    if request.method == "POST" and form.validate_on_submit():
        try:
            patient = get_db().get_patients_by_id(form.patient.data)
            doctor = get_db().get_user_by_id(form.doctor.data)
            status = 0
            time = form.appointment_time.data
            if doctor.id == current_user.id:
                status = 1
            location = get_db().get_medical_room_by_room_number(form.location.data)
            description = form.description.data
            
            new_appointment = Appointments(
                patient, doctor, time, status, location, description)

            new_id = get_db().add_appointment(new_appointment)
            flash("Appointement added to the List of Appointments")
            return redirect(url_for(f"{user}.dashboard"))
        except DatabaseError as e:
            flash("something went wrong with the database")
            return redirect('home.index')

    return render_template('appointments.html', form=form)

@bp.route('/<int:id>/')
@login_required
@patient_access
def get_appointment(id):
    form = AppointmentResponseForm()
    form.set_choices()
    try:
        db = get_db()
        appointment = db.get_appointment_by_id(id)
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('home.index')
    if appointment is None:
        flash("Appointment cannot be found", 'error')
        return redirect(url_for('appointments.book_appointment'))
    return render_template('specific_appointment.html', appointment=appointment, form=form)


@bp.route('/confirmed/<string:user_type>/')
@login_required
@patient_access
def confirmed_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('home.index'))
    try:
        appointments = None
        if user_type == 'doctor':
            appointments = get_db().get_appointments_by_status_doctor(1, current_user.id)
        if user_type == 'patient':
            appointments = get_db().get_appointments_by_status_patient(1, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for(f'{user_type}.dashboard'))
        return render_template('confirmed_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for(f'{user_type}.dashboard'))
    except ValueError as e:
        flash("Parameter values are incorrect")
        return redirect(url_for(f'{user_type}.dashboard'))


@bp.route('/requests/<string:user_type>/')
@login_required
@patient_access
def requested_appointments(user_type):
    if user_type not in ('doctor', 'patient'):
        flash("Incorrect user type")
        return redirect(url_for('home.index'))
    try:
        appointments = None
        if user_type == 'doctor':
            appointments = get_db().get_appointments_by_status_doctor(0, current_user.id)
        if user_type == 'patient':
            appointments = get_db().get_appointments_by_status_patient(0, current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for(f'{user_type}.dashboard'))
        return render_template('requested_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for(f'{user_type}.dashboard'))
    except ValueError as e:
        flash("Parameter values are incorrect")
        return redirect(url_for(f'{user_type}.dashboard'))

# CHANGE!!!
@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
@login_required
@patient_access
def update_appointment(id):
    form = AppointmentResponseForm()
    form.set_choices()
    try:
        appointment = get_db().get_appointment_by_id(id)
        if request.method == 'POST' and form.validate_on_submit():
            status = form.select_confirmation.data
            room = form.room.data
            get_db().update_appointment_status(id, status, room=room)
            flash("Appointment has been successfully updated")
            return redirect(url_for('appointments.requested_appointments', user_type='doctor'))
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect(url_for('appointments.requested_appointments', user_type='doctor'))
    except TypeError as e:
        flash("Incorrect types")
        return redirect(url_for('appointments.requested_appointments', user_type='doctor'))
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('appointments.requested_appointments', user_type='doctor'))

    if appointment is None:
        abort(404, "This address does not exist")
    return render_template('specific_appointment.html', appointment=appointment, form=form)
