from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from .db.dbmanager import get_db
import urllib.parse


bp = Blueprint('doctor_api', __name__, url_prefix='/api/doctors/')


def login_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def patient_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'PATIENT' and current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN' and current_user.access_level != 'ADMIN_USER':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('', methods=['GET'])
def get_doctors():
    doctors = []
    page = None
    if request.args:
        page = request.args.get("page")
        if page is None:
            page = 1
        try:
            page = int(page)
        except:
            abort(make_response(
                jsonify(id="400", description="The page number is of incorrect type"), 400))
        first_name = request.args.get("first")
        last_name = request.args.get("last")

        if last_name is not None and not isinstance(last_name, str) or first_name is not None and not isinstance(first_name, str):
            abort(make_response(jsonify(
                id="400", description="The the first or last names are of incorrect type"), 400))
        try:
            doctors = get_db().get_doctors_page_number(page, first_name, last_name)
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description=[
                  'Something went wrong with our database']), 409))
        except TypeError as e:
            abort(make_response(
                jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError as e:
            abort(make_response(
                jsonify(id="400", description="The data sent cannot be empty"), 400))

    else:
        try:
            page = 1
            doctors = get_db().get_doctors_page_number(page, None, None)
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description=[
                  'Something went wrong with our database']), 409))

    if doctors is None or len(doctors) == 0:
        abort(make_response(jsonify(
            id="404", description="No doctors currently available in the database"), 404))

    data = {}
    count = len(get_db().get_doctors())
    data['count'] = count
    data['previous'] = urllib.parse.urljoin(request.url_root, url_for(
        'doctor_api.get_doctors', page=(page-1))) if page > 1 else ""
    data['next'] = urllib.parse.urljoin(request.url_root, url_for(
        'doctor_api.get_doctors', page=(page+1))) if count % 10 != 0 and len(doctors) >= 10 else ""
    data['results'] = []
    for doctor in doctors:
        data['results'].append(doctor.to_json(request.url_root))

    return jsonify(data)


@bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    doctor = None
    try:
        doctor = get_db().get_doctor_by_id(doctor_id)
        if doctor == None:
            abort(make_response(jsonify(
                id="404", description="The doctor you are trying to query does not exist"), 404))

    except DatabaseError as e:
        abort(make_response(jsonify(id="409", description=[
              'Something went wrong with our database']), 409))
    except TypeError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent is of incorrect type"), 400))
    except ValueError as e:
        abort(make_response(
            jsonify(id="400", description="The data sent cannot be empty"), 400))

    doctor_json = doctor.to_json(request.url_root)
    return jsonify(doctor_json)
