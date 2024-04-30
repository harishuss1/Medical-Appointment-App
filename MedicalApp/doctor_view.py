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
    


