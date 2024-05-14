import json
from flask import Blueprint, jsonify, make_response, request, render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from oracledb import DatabaseError
from MedicalApp.allergy import Allergy
from MedicalApp.forms import PatientDetailsForm
from MedicalApp.user import MedicalPatient
from .db.dbmanager import get_db

bp = Blueprint('medical_rooms_api', __name__, url_prefix="/api/medical_rooms/")

@bp.route('/', methods=['GET'])
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