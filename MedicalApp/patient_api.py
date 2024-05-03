import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
# from .forms import PatientForm   will implement this later for updating

bp = Blueprint('patient_api', __name__, url_prefix="/api/patients/")

@bp.route('/', methods=['GET'])
def get_patients():
    patients = []
    if request.args:
        page = int(request.args.get("page"))
        
        if page is None or not isinstance(page, int):
            abort(400, "Query parameters incorrect")
            
        patients = get_db().get_patients_page_number(page)
    else:
        patients = get_db().get_patients()
    data = {}
    data['results'] = []
    for patient in patients:
        data['results'].append(patient.to_json())
    return jsonify(data)
