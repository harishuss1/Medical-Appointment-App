from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from MedicalApp.appointments import Appointments
from MedicalApp.forms import AppointmentForm
from MedicalApp import db, dbmanager

bp = Blueprint('appointments', __name__, url_prefix='/appointments/')


@bp.route('', methods=['GET', 'POST'])
def get_appointments():
    db = dbmanager.get_db()
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
        new_appointment = Appointments(id, patient_id, doctor_id, appointment_id, status, location, description)

        # checks if theres any existing appointment in the appointments list and it will check if it matches with
        # the new appointment, if match then it flashed that it already exist and
        # will not take the new appointment
        if any(appointment.id == new_appointment.id and
               appointment.patient_id == new_appointment.patient_id_id and
               appointment.doctor_id == new_appointment.doctor_id
               for appointment in appointments):
            flash("Appointment already exists", "error")
        else:
            new_appointment = Appointments(id, patient_id, doctor_id, appointment_id, status, location, description)
            db.add_appointment(new_appointment)
            flash("Appointement added to the List of Appointments")

            return redirect(
                url_for('appointments.get_appointment', id=new_appointment.id))

    return render_template('appointments.html', appointments=appointments, form=form)


@bp.route('/<int:id>/')
def get_appointment(id):
    db = dbmanager.get_db()
    appointment = db.get_address(id)
    if appointment is None:
        flash("Appointment cannot be found", 'error')
        return redirect(url_for('appointments.get_appointments'))
    return render_template('specific_appointment.html', appointment=appointment)

