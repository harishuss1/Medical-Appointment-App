import json
from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError, IntegrityError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
import urllib.parse

bp = Blueprint('patient_api', __name__, url_prefix="/api/patients")

def login_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def patient_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# supports first= last= and page=. page defaults to 1 if none is specified
@bp.route('', methods=['GET'])
@login_required
@patient_access
def get_patients():
    patients = []
    page = None
    if request.args:
        page = request.args.get("page")
        if page is None:
            page = 1
        try:
            page = int(page) 
        except:
            abort(make_response(jsonify(id="400", description="The page number is of incorrect type"), 400))
        first_name = request.args.get("first")
        last_name = request.args.get("last")

        if last_name is not None and not isinstance(last_name, str) or first_name is not None and not isinstance(first_name, str):
            abort(make_response(jsonify(id="400", description="The the first or last names are of incorrect type"), 400))
        try:
            patients = get_db().get_patients_page_number(page, first_name, last_name)
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
        except TypeError as e:
            abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError as e:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))

    else:
        try:
            page = 1
            patients = get_db().get_patients_page_number(page, None, None)
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))

    if patients is None or len(patients) == 0:
        abort(make_response(jsonify(id="404", description="No patients currently available in the database"), 404))
        
    data = {}
    count = len(get_db().get_patients())
    data['count'] = count
    data['previous'] = urllib.parse.urljoin(request.url_root, url_for('patient_api.get_patients', page=(page-1))) if page > 1 else ""
    data['next'] = urllib.parse.urljoin(request.url_root, url_for('patient_api.get_patients', page=(page+1))) if count%10 !=0 and len(patients) >= 10 else ""
    data['results'] = []
    for patient in patients:
        data['results'].append(patient.to_json(request.url_root))

    return jsonify(data)

#{ allergies: [] } -> list of allergy ids : return 201 when successful
@bp.route('/<int:patient_id>', methods=['GET', 'PUT'])
@login_required
@patient_access
def get_patient(patient_id):
    patient = None
    try:
        patient = get_db().get_patients_by_id(patient_id)
        if patient == None:
            abort(make_response(jsonify(id="404", description="The patient you are trying to query does not exist"), 404))

        if request.method == 'PUT':
            json_data = request.json
            allergy_ids = []
            try:
                json_data['allergies']
            except:
                abort(make_response(jsonify(id="400", description=f"No allergies parameter found."), 400))
                
            for allergy in patient.allergies:
                allergy_ids.append(allergy.id)

            for a in json_data['allergies']:
                allergy_id = None
                try:
                    allergy_id = int(a)
                except:
                    abort(make_response(jsonify(id="400", description=f"The allergy id {allergy_id} is of incorrect type."), 400))
                allergy = get_db().get_allergy_by_id(allergy_id)
                if allergy is None:
                    abort(make_response(jsonify(id="404", description=f"The allergy id {allergy_id} does not exist."), 404))
                if allergy_id not in allergy_ids:
                    allergy_ids.append(allergy_id)

            get_db().update_allergies(patient_id, allergy_ids)

            resp = make_response(get_db().get_patients_by_id(patient_id).to_json(request.url_root), 201)
            return resp
    except IntegrityError as e:
        abort(make_response(jsonify(id="400", description='The allergie(s) you have provided do not exist'), 400))
    except DatabaseError as e:
        abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
    except TypeError as e:
        abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
    except ValueError as e:
        abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))

    patient_json = patient.to_json(request.url_root)
    return jsonify(patient_json)