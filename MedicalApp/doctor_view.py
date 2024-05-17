from flask import (Blueprint, render_template, redirect,
                   flash, url_for, request, abort)
from .user import User
from .db.dbmanager import get_db
from oracledb import InternalError, DatabaseError
from flask_login import current_user, login_user, logout_user, login_required
from .forms import AllergyForm, AppointmentResponseForm
from .db.db import Database

bp = Blueprint('doctor', __name__, url_prefix="/doctor/")

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('/')
@login_required
@doctor_access
def dashboard():
    return render_template("doctor.html")


@bp.route('/patients/')
@login_required
@doctor_access
def patients():
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
@doctor_access
def notes(patient_id):
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
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('doctor.dashboard'))
    

@bp.route('/allergies/add', methods=['GET', 'POST'])
@login_required
@doctor_access
def add_allergy():
    form = AllergyForm()
    if form.validate_on_submit():
        try:
            get_db().add_allergy(form.name.data, form.description.data)
            flash('Allergy has been successfully added')
            return redirect(url_for('doctor.dashboard'))
        except DatabaseError as e:
            flash("Something went wrong with the database")
            return redirect(url_for('doctor.dashboard'))
    return render_template('add_allergy.html', form=form)

