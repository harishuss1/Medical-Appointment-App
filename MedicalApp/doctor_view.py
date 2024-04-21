from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError

bp = Blueprint('doctor', __name__, url_prefix="/doctor/")

@bp.route('/')
def dashboard():
    return render_template("doctor.html")

@bp.route('/appointments/')
def confirmed_appointments():
    try:
        appointments = get_db().get__appointments_by_status(1)
        if appointments is None:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_appointments.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))

@bp.route('/requests/')
def requested_appointments():
    try:
        appointments = get_db().get__appointments_by_status(1)
        if appointments is None:
            flash("No confirmed appointments")
            return redirect(url_for('doctor.dashboard'))
        return render_template('doctor_requests.html', appointments=appointments)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('doctor.dashboard'))

@bp.route('/notes/')
def notes():
    return render_template('doctor_notes.html')