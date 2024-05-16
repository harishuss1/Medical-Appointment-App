import json
from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db
import urllib.parse

bp = Blueprint('allergy_api', __name__, url_prefix="/api/allergies")


@bp.route('', methods=['GET'])
def get_allergies():
    allergies = []
    page = None
    try:
        if request.args:
            page = request.args.get("page")
            if page is None:
                page = 1
            try:
                page = int(page) 
            except:
                abort(make_response(jsonify(id="400", description="The page number is of incorrect type"), 400))
            
            name = request.args.get("name")

            if name is not None and not isinstance(name, str):
                abort(make_response(
                jsonify(id="400", description=f"The allergy name is of incorrect type."), 400))
            
            allergies = get_db().get_allergies_page_number(page, name)

        else:
            page = 1
            allergies = get_db().get_allergies_page_number(page, None)

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
    count = len(get_db().get_all_allergies())
    data['count'] = count
    data['previous'] = urllib.parse.urljoin(request.url_root, url_for('allergy_api.get_allergies', page=(page-1))) if page > 1 else ""
    data['next'] = urllib.parse.urljoin(request.url_root, url_for('allergy_api.get_allergies', page=(page+1))) if count%10 !=0 and len(allergies) >= 10 else ""
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
