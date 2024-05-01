from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
# from .forms import PatientForm   will implement this later for updating

bp = Blueprint('patient', __name__, url_prefix="/patients")

def patient_access(func):
    def wrapper():
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(401, "You do not have access to this page!")
        func()
    wrapper.__name__ = func.__name__
    return wrapper


@bp.route('/')
@login_required
@patient_access
def patient_dashboard():
    if current_user.access_level != 'PATIENT':
        flash("You do not have permission to access this page.")
        return redirect(url_for('home.index'))

    appointments = get_db().get_patient_appointments(current_user.id)
    return render_template('patient_dashboard.html', appointments=appointments)

@bp.route('/details/update/', methods=['GET', 'POST'])
@login_required
@patient_access
def update_patient():
    form = PatientDetailsForm()

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

    return render_template('update_patient.html', form=form)


@bp.route('/details/', methods=['GET'])
@login_required
def view_patient():
    patient_details = get_db().get_patient_details(current_user.id)

    if patient_details is None:
        flash("No patient details found.")
        return redirect(url_for('home.index'))

    patient = MedicalPatient(weight=patient_details.weight, email=patient_details.email, password=patient_details.password, first_name=patient_details.first_name, last_name=patient_details.last_name,
                             access_level=patient_details.access_level, dob=patient_details.dob, blood_type=patient_details.blood_type, height=patient_details.height, avatar_path=patient_details.avatar_path, id=patient_details.id)

    patient.allergies = get_db().get_patient_allergies(patient.id)

    return render_template('patient_details.html', patient=patient)
