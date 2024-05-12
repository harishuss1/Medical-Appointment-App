import json
from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('allergy_api', __name__, url_prefix="/api/allergies")


@bp.route('', methods=['GET'])
def get_allergies():
    allergies = []
    try:
        if request.args:
            page = int(request.args.get("page")) if request.args.get("page").isdigit() else abort(make_response(jsonify(id="400", description="The page number is of incorrect type"), 400))
            name = str(request.args.get("name"))

            if page is None or not isinstance(page, int):
                page = 1

            if name is not None and not isinstance(name, str):
                abort(make_response(
                jsonify(id="400", description=f"The allergy name is of incorrect type."), 400))
                
            allergies = get_db().get_allergies_page_number(page, name)

        else:
            allergies = get_db().get_allergies_page_number(1, None)

    except DatabaseError as e:
        abort(make_response(
            jsonify(id="409", description="Something went wrong with our database"), 409))
    except TypeError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent is of incorrect type"), 400))
    except ValueError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent cannot be empty"), 400))

    if allergies is None or len(allergies) == 0:
        abort(make_response(jsonify(
            id="404", description=f"There are currently no allergies in the database"), 404))

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
            abort(make_response(
                jsonify(id="404", description=f"The allergy id {allergy_id}"), 404))

        allergy_json = allergy.to_json()
        return jsonify(allergy_json)

    except DatabaseError as e:
        abort(make_response(
            jsonify(id="409", description="Something went wrong with our database"), 409))
    except TypeError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent is of incorrect type"), 400))
    except ValueError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent cannot be empty"), 400))
