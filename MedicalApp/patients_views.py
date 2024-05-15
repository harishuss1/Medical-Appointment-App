from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
# from .forms import PatientForm   will implement this later for updating

bp = Blueprint('patient', __name__, url_prefix="/patients/")

def patient_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


@bp.route('/')
@login_required
@patient_access
def dashboard():
    try:
        appointments = get_db().get_patient_appointments(current_user.id)
        if appointments is None or len(appointments) == 0:
            flash("No appointments are currently under your name!")
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('home.index'))
    return render_template('patient_dashboard.html', appointments=appointments)

@bp.route('/details/update/', methods=['GET', 'POST'])
@login_required
@patient_access
def update_patient():
    form = PatientDetailsForm()
    try:
        allergies = get_db().get_all_allergies()
        form.allergies.choices = [(Allergy['id'], Allergy['name'])
                              for Allergy in allergies]
        if request.method == 'POST' and form.validate_on_submit():
            dob = form.dob.data
            blood_type = form.blood_type.data
            height = form.height.data
            weight = form.weight.data
            selected_allergies = form.allergies.data  # Storing ids

            get_db().update_patient_details(current_user.id, dob,
                                            blood_type, height, weight, selected_allergies)

            patient_allergies = get_db().get_patient_allergies(current_user.id)
            form.allergies.data = [Allergy.id for Allergy in patient_allergies]

            flash('Your information has been updated.')
            return redirect(url_for('patient.view_patient'))
    except DatabaseError as e:
        flash("something went wrong with the database")
        return redirect('home.index')
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('home.index'))
    form.prefill()
    return render_template('update_patient.html', form=form)


@bp.route('/details/', methods=['GET'])
@login_required
def view_patient():
    try:
        patient_details = get_db().get_patient_details(current_user.id)

        if patient_details is None:
            flash("No patient details found.")
            return redirect(url_for('home.index'))

        patient = MedicalPatient(weight=patient_details.weight, email=patient_details.email, password=patient_details.password, first_name=patient_details.first_name, last_name=patient_details.last_name,
                                access_level=patient_details.access_level, dob=patient_details.dob, blood_type=patient_details.blood_type, height=patient_details.height, avatar_path=patient_details.avatar_path, id=patient_details.id)

        patient.allergies = get_db().get_patient_allergies(patient.id)
    except DatabaseError as e:
        flash("Something went wrong with the database")
        return redirect(url_for('home.index'))
    except ValueError as e: 
        flash("Incorrect values were passed")
        return redirect(url_for('home.index'))

    return render_template('patient_details.html', patient=patient)


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