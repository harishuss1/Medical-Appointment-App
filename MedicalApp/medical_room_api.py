import json
from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import current_user
from oracledb import DatabaseError, IntegrityError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

def login_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

def doctor_access(func):
    def wrapper(*args, **kwargs):
        if current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN':
            return abort(403, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

bp = Blueprint('medical_rooms_api', __name__, url_prefix="/api/medical_rooms")

@bp.route('', methods=['GET', 'POST'])
@login_required
def get_medical_rooms():
    medical_rooms = []
    if request.args:
        page = request.args.get("page")
        if page is None:
            page = 1
        try:
            page = int(page) 
        except:
            abort(make_response(jsonify(id="400", description="The page number is of incorrect type"), 400))
        room_number = str(request.args.get("room"))

        if room_number is not None and not isinstance(room_number, str):
            abort("Query parameters incorrect")
        try:
            medical_rooms = get_db().get_medical_room_page_number(page, room_number)
        except DatabaseError as e:
            abort(409)
        except TypeError as e:
            abort(400, "The data sent is of incorrect type")
        except ValueError as e:
            abort(400, "The data sent cannot be empty")
            
    elif request.method == 'POST':
        if (current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN'):
            abort(make_response(jsonify(id="403", description='You do not have access to this page!'), 403))
            
        json_data = request.json
        try:
            room_number = json_data['room_number']
            description = json_data['description']
        except:
            abort(make_response(jsonify(id="400", description=f"No room number or description parameter found."), 400))
        if room_number == "" or description == "":
            abort(make_response(jsonify(id="400", description=f"Empty room number or description params."), 400))
        try:
            get_db().add_medical_room(room_number, description)
            resp = make_response({}, 201)
            resp.headers['Room'] = url_for('medical_rooms_api.get_room_number', room_number=room_number)
            return resp
        except IntegrityError as e:
            abort(make_response(jsonify(id="400", description='The room you have provided already exists'), 400))
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
        except TypeError as e:
            abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError as e:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
        
    else:
        try:
            medical_rooms = get_db().get_medical_rooms()
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description=['Something went wrong with our database']), 409))

    if medical_rooms is None or len(medical_rooms) == 0:
        abort(404)
    data = {}
    data['results'] = []
    for medical_room in medical_rooms:
        data['results'].append(medical_room.to_json())

    return jsonify(data)

@bp.route('/<string:room_number>', methods=['GET'])
@login_required
def get_room_number(room_number):
    room = None
    try:
        room = get_db().get_medical_room_by_room_number(room_number)
        if room == None:
            abort(404)

        room_json = room.to_json()
        return jsonify(room_json)

    except DatabaseError as e:
        abort(409)
    except TypeError as e:
            abort(400, "The data sent is of incorrect type")
    except ValueError as e:
        abort(400, "The data sent cannot be empty")