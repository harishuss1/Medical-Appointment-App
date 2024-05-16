import datetime
from flask import Blueprint, Response, abort, jsonify, make_response, request
from flask_login import current_user
from oracledb import DatabaseError, IntegrityError
from .db.dbmanager import get_db
from MedicalApp.appointments import Appointments

bp = Blueprint('appointments_api', __name__, url_prefix='/api/appointments/')

def login_required(func):
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            return abort(401, "You do not have access to this page!")
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper

@bp.route('', methods=['GET', 'POST'])
def get_appointments_api():
    if request.method == 'POST':
        appointment = Appointments.from_json(request.json)
        get_db().add_appointment(appointment)
        return jsonify(message="Appointment added successfully"), 201

    if request.args:
        page = int(request.args.get("page", 1))
        id = request.args.get("id")

        if id:
            appointment = get_db().get_appointment_by_id(id)
            if appointment:
                return jsonify({
                    "id": appointment.id,
                    "patient": appointment.patient.to_json(),
                    "doctor": appointment.doctor.to_json(),
                    "appointment_time": appointment.appointment_time.isoformat(),
                    "location": appointment.location.to_json(),
                    "description": appointment.description
                })
            else:
                abort(404)
        else:
            abort(400)

    appointments = get_db().get_appointments()
    json_appointments = [{
        "id": appointment.id,
        "patient": appointment.patient.to_json(()),
        "doctor": appointment.doctor.to_json(),
        "appointment_time": appointment.appointment_time.isoformat(),
        "location": appointment.location.to_json(),
        "description": appointment.description
    } for appointment in appointments]
    return jsonify(json_appointments)


@bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_appointment_by_id_api(id):
    appointment = get_db().get_appointment_by_id(id)
    if request.method == 'GET':
        try:
            appointment = get_db().get_appointment_by_id(id)
            if appointment:
                return jsonify(appointment.to_dict())
            else:
                abort(404)
        except Exception:
            abort(500)
    
    elif request.method == 'PUT':
        if appointment.status != 0:
            abort(make_response(jsonify(id="400", description='You cannot update an appointment that is not pending'), 400))
        appointment_json = request.json
        if appointment_json:
            
            try:
                # Check if the current user is a patient or a doctor
                if current_user.access_level == 'PATIENT':
                    if ('doctor' not in appointment_json and 'appointment_time' not in appointment_json and 'description' not in appointment_json):
                        abort(make_response(jsonify(id="400", description='You have not provided the correct fields to update'), 400))
                    # Patient can only update appointment_time and description
                    if 'doctor' in appointment_json:
                        try:
                            doctor_id = int(appointment_json['doctor_id'])
                            doctor = get_db().get_user_by_id(doctor_id)
                            if doctor is None:
                                abort(make_response(jsonify(id="404", description='Doctor does not exist'), 404))
                            if doctor.access_level != 'STAFF' and doctor.access_level != 'ADMIN':
                                abort(make_response(jsonify(id="400", description='User provided is not a doctor'), 400))
                        except:
                            abort(make_response(jsonify(id="400", description='Incorrect type for doctor id'), 400))
                    if 'time' in appointment_json:
                        time = appointment_json['appointment_time']
                        try:
                            datetime_object = datetime.strptime(time, '%Y-%m-%d')
                            appointment.appointment_time = datetime_object
                        except:
                            abort(make_response(jsonify(id="400", description='Date provided is invalid. use YYYY-MM-DD format.'), 400))
                    if 'description' in appointment_json:
                        description = appointment_json['description']
                        appointment.description = description
                    
                elif current_user.access_level == 'STAFF':
                    # Doctor can only update status and location
                    if ('status' not in appointment_json and 'location' not in appointment_json):
                        abort(make_response(jsonify(id="400", description='You have not provided the correct fields to update'), 400))
                    status = None
                    if 'status' in appointment_json:
                        try:
                            status = int(appointment_json['status'])
                            appointment.status = status
                        except:
                            abort(make_response(jsonify(id="400", description='Invalid status has been provided'), 400))
                    if 'location' in appointment_json:
                        location = get_db().get_medical_room_by_room_number(appointment_json['location'])
                        if location is None:
                            abort(make_response(jsonify(id="404", description='The room you have provided do not exist'), 404))
                        appointment.location = location
                get_db().update_appointment(appointment)
                return jsonify(message="Appointment updated successfully"), 200
            except IntegrityError as e:
                abort(make_response(jsonify(id="400", description='The allergie(s) you have provided do not exist'), 400))
            # except DatabaseError as e:
            #     abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
            except TypeError as e:
                abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
            except ValueError as e:
                abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
        else:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
    elif request.method == 'DELETE':
        try:
            get_db().delete_appointment_by_id(id)
            return jsonify(message="Appointment deleted successfully"), 200
        except Exception:
            abort(500)
