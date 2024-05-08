import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('patient_api', __name__, url_prefix="/api/patients/")

# supports first= last= and page=. page defaults to 1 if none is specified
@bp.route('/', methods=['GET'])
def get_patients():
    patients = []
    if request.args:
        page = int(request.args.get("page"))
        first_name = str(request.args.get("first"))
        last_name = str(request.args.get("last"))

        if page is None or not isinstance(page, int):
            page = 1

        if last_name is not None and not isinstance(last_name, str) or first_name is not None and not isinstance(first_name, str):
            abort("Query parameters incorrect")
        try:
            patients = get_db().get_patients_page_number(page, first_name, last_name)
        except DatabaseError as e:
            abort(409)
        except TypeError as e:
            abort(400, "The data sent is of incorrect type")
        except ValueError as e:
            abort(400, "The data sent cannot be empty")

    else:
        try:
            patients = get_db().get_patients()
        except DatabaseError as e:
            abort(409)

    if patients is None or len(patients) == 0:
        abort(404)
    data = {}
    data['results'] = []
    for patient in patients:
        data['results'].append(patient.to_json())

    return jsonify(data)
