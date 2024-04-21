from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import login_user, logout_user, login_required
from .forms import AppointmentResponseForm

bp = Blueprint('doctor', __name__, url_prefix="/doctor/")


@bp.route('/')
#@login_required
def dashboard():
    return render_template("doctor.html")


@bp.route('/appointments/')
#@login_required
def confirmed_appointments():
    try:
        appointments = get_db().get__appointments_by_status(1)
        if appointments is None or len(appointments) == 0:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/')
#@login_required
def requested_appointments():
    try:
        appointments = get_db().get__appointments_by_status(0)
        if appointments is None or len(appointments) == 0:
            flash("No requested appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_requests.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))


@bp.route('/requests/<int:id>/', methods=['GET', 'POST'])
#@login_required
def update_appointment(id):
    form = AppointmentResponseForm()
    appointment = get_db().get__appointment_by_id(id)

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


@bp.route('/notes/')
@login_required
def notes():
    return render_template('doctor_notes.html')
