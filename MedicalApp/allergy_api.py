import json
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('allergy_api', __name__, url_prefix="/api/allergies/")

@bp.route('/', methods=['GET'])
def get_allergies():
    allergies = []
    if request.args:
        page = int(request.args.get("page"))
        name = str(request.args.get("name"))

        if page is None or not isinstance(page, int):
            page = 1

        if name is not None and not isinstance(name, str):
            abort("Query parameters incorrect")
        try:
            allergies = get_db().get_allergies_page_number(page, name)
        except DatabaseError as e:
            abort(409)
        except TypeError as e:
            abort(400, "The data sent is of incorrect type")
        except ValueError as e:
            abort(400, "The data sent cannot be empty")

    else:
        try:
            allergies = get_db().get_allergies_page_number(1, None)
        except DatabaseError as e:
            abort(409)

    if allergies is None or len(allergies) == 0:
        abort(404)
    data = {}
    data['results'] = []
    for allergy in allergies:
        data['results'].append(allergy.to_json())

    return jsonify(data)


@bp.route('/<int:allergy_id>', methods=['GET'])
def get_allergy(allergy_id):
    allergy = None
    try:
        allergy = get_db().get_allergy_by_id(allergy_id)
        if allergy == None:
            abort(404)

        allergy_json = allergy.to_json()
        return jsonify(allergy_json)

    except DatabaseError as e:
        abort(409)
    except TypeError as e:
            abort(400, "The data sent is of incorrect type")
    except ValueError as e:
        abort(400, "The data sent cannot be empty")