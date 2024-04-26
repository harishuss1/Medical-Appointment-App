from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from MedicalApp.forms import PatientDetailsForm
from .db.dbmanager import get_db
# from .forms import PatientForm   will implement this later for updating

bp = Blueprint('patient', __name__, url_prefix="/patients")


@bp.route('/')
@login_required
def patient_dashboard():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_dashboard.html', appointments=appointments)


@bp.route('/appointments')
@login_required
def view_appointments():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_appointments.html', appointments=appointments)


@bp.route('/details', methods=['GET', 'POST'])
@login_required
def update_patient():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    form = PatientDetailsForm()

    if request.method == 'POST' and form.validate_on_submit():
        dob = form.dob.data
        blood_type = form.blood_type.data
        height = form.height.data
        weight = form.weight.data

        get_db().update_patient_details(current_user.id, dob, blood_type, height, weight)

        flash('Your information has been updated.')
        return redirect(url_for('patient.patient_dashboard'))

    return render_template('update_patient.html', form=form)
