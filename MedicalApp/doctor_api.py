from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from .db.dbmanager import get_db


bp = Blueprint('doctor_api', __name__, url_prefix="/api/doctors/")


@bp.route('/', methods=['GET'])
def get_doctors():
    doctors = []
    if request.args:
        page = int(request.args.get("page")) if request.args.get(
            "page").isdigit() else abort(400, "The data sent is of incorrect type")
        first_name = request.args.get("first")
        last_name = request.args.get("last")

        if page is None:
            page = 1

        if last_name is not None and not isinstance(last_name, str) or first_name is not None and not isinstance(first_name, str):
            abort("Query parameters incorrect")
        try:
            doctors = get_db().get_doctors_page_number(page, first_name, last_name)
        except DatabaseError as e:
            abort(409)
        except TypeError as e:
            abort(400, "The data sent is of incorrect type")
        except ValueError as e:
            abort(400, "The data sent cannot be empty")

    else:
        try:
            doctors = get_db().get_doctors_page_number(1, None, None)
        except DatabaseError as e:
            abort(409)

    if doctors is None or len(doctors) == 0:
        abort(404)

    data = {}
    data['results'] = []
    for doctor in doctors:
        data['results'].append(doctor.to_json(request.url_root))

    return jsonify(data)


@bp.route('/<int:doctor_id>/', methods=['GET'])
def get_doctor(doctor_id):
    doctor = None
    try:
        doctor = get_db().get_doctors_by_id(doctor_id)
        if doctor == None:
            abort(404)

        doctor_json = doctor.to_json(request.url_root)
        return jsonify(doctor_json)

    except DatabaseError as e:
        abort(409)
    except TypeError as e:
        abort(400, "The data sent is of incorrect type")
    except ValueError as e:
        abort(400, "The data sent cannot be empty")
