import datetime
from flask import Blueprint, Response, abort, jsonify, make_response, redirect, request, url_for
from flask_login import current_user
from oracledb import DatabaseError, IntegrityError
from .db.dbmanager import get_db
from MedicalApp.appointments import Appointments
from datetime import datetime
import urllib.parse


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
        appointment_json = request.json
        try:
            if ('doctor_id' not in appointment_json and 'appointment_time' not in appointment_json and 'description' not in appointment_json):
                    abort(make_response(jsonify(id="400", description='You have not provided the correct fields to update'), 400))
            try:
                doctor_id = int(appointment_json['doctor_id'])
                doctor = get_db().get_user_by_id(doctor_id)
                if doctor is None:
                    abort(make_response(jsonify(id="404", description='Doctor does not exist'), 404))
                if doctor.access_level != 'STAFF' and doctor.access_level != 'ADMIN':
                    abort(make_response(jsonify(id="400", description='User provided is not a doctor'), 400))
            except:
                abort(make_response(jsonify(id="400", description='Incorrect type for doctor id'), 400))
            time = appointment_json['appointment_time']
            try:
                datetime_object = datetime.strptime(time, '%Y-%m-%d')
            except:
                abort(make_response(jsonify(id="400", description='Date provided is invalid. use YYYY-MM-DD format.'), 400))
            description = appointment_json['description']

            if current_user.access_level == 'PATIENT':
                patient = get_db().get_patients_by_id(current_user.id)
                room = get_db().get_medical_room_by_room_number('101')
                appointment = Appointments(patient, doctor, datetime_object, 0, room, description) #default room location of 101

            elif current_user.access_level == 'STAFF' or current_user.access_level == 'ADMIN':
                if ('patient' not in appointment_json and 'location' not in appointment_json):
                    abort(make_response(jsonify(id="400", description='You have not provided the correct fields to update'), 400))
                try:
                    patient_id = int(appointment_json['patient_id'])
                    patient = get_db().get_patients_by_id(patient_id)
                    if patient is None:
                        abort(make_response(jsonify(id="404", description='Doctor does not exist'), 404))
                except:
                    abort(make_response(jsonify(id="400", description='Incorrect type for doctor id'), 400))

                location = get_db().get_medical_room_by_room_number(appointment_json['location'])
                if location is None:
                    abort(make_response(jsonify(id="404", description='The room you have provided do not exist'), 404))
                
                if current_user.id == doctor.id:
                    status = 1
                else:
                    status = 0
                appointment = Appointments(patient, doctor, datetime_object, status, location, description)
                

            appt_id = get_db().add_appointment(appointment)
            appointment = get_db().get_appointment_by_id(appt_id)

        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
        except TypeError as e:
            abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError as e:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
        except Exception as e:
            abort(make_response(jsonify(id="400", description="You have not given us all parameters necessary. Please review your request."), 400))
        
        appointment_json = appointment.to_json(request.url_root)
        resp = make_response(appointment_json,201)
        return resp

    if request.args:
        page = int(request.args.get("page", 1))
        doctor_first_name = request.args.get("doctor_first_name")
        doctor_last_name = request.args.get("doctor_last_name")
        patient_first_name = request.args.get("patient_first_name")
        patient_last_name = request.args.get("patient_last_name")

        try:
            appointments = get_db().get_appointments_page_number(page, doctor_first_name, doctor_last_name, patient_first_name, patient_last_name)
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
        except TypeError as e:
            abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError as e:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))

        if not appointments:
            abort(make_response(jsonify(id="404", description="No appointments found"), 404))

        data = {}
        count = len(get_db().get_appointments())
        data['count'] = count
        data['previous'] = urllib.parse.urljoin(request.url_root, url_for('appointment_api.get_appointments_api', page=(page-1))) if page > 1 else ""
        data['next'] = urllib.parse.urljoin(request.url_root, url_for('appointment_api.get_appointments_api', page=(page+1))) if (count - (page * 10)) > 0 else ""
        data['results'] = [appointment.to_json() for appointment in appointments]

        return jsonify(data)
    
    else:
        try:
            appointments = get_db().get_appointments()
        except DatabaseError as e:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))

        data = {}
        data['results'] = [appointment.to_json(request.url_root) for appointment in appointments]
        return jsonify(data)



@bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def get_appointment_by_id_api(id):
    appointment = get_db().get_appointment_by_id(id)
    if request.method == 'GET':
        appointment = get_db().get_appointment_by_id(id)
        if appointment:
            return jsonify(appointment.to_dict())
        else:
            abort(404)
    
    elif request.method == 'PUT':
        if appointment.status != 0:
            abort(make_response(jsonify(id="400", description='You cannot update an appointment that is not pending'), 400))
        appointment_json = request.json
        if appointment_json:
            
            try:
                # Check if the current user is a patient or a doctor
                if current_user.access_level == 'PATIENT':
                    if ('doctor_id' not in appointment_json and 'appointment_time' not in appointment_json and 'description' not in appointment_json):
                        abort(make_response(jsonify(id="400", description='You have not provided the correct fields to update'), 400))
                    # Patient can only update appointment_time and description
                    if 'doctor_id' in appointment_json:
                        try:
                            doctor_id = int(appointment_json['doctor_id'])
                            doctor = get_db().get_user_by_id(doctor_id)
                            if doctor is None:
                                abort(make_response(jsonify(id="404", description='Doctor does not exist'), 404))
                            if doctor.access_level != 'STAFF' and doctor.access_level != 'ADMIN':
                                abort(make_response(jsonify(id="400", description='User provided is not a doctor'), 400))
                            appointment.doctor = doctor
                        except:
                            abort(make_response(jsonify(id="400", description='Incorrect type for doctor id'), 400))
                    if 'appointment_time' in appointment_json:
                        time = appointment_json['appointment_time']
                        try:
                            datetime_object = datetime.strptime(time, "%Y-%m-%d")
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
                resp = make_response({}, 201)
                resp.headers['Appointment'] = url_for('appointments_api.get_appointment_by_id_api', id=id)
                return resp
            except IntegrityError as e:
                abort(make_response(jsonify(id="400", description='The allergie(s) you have provided do not exist'), 400))
            except DatabaseError as e:
                abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
            except TypeError as e:
                abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
            except ValueError as e:
                abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
        else:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
    elif request.method == 'DELETE':
        if(current_user.access_level != 'STAFF' and current_user.access_level != 'ADMIN'):
            return abort(403, "You do not have access to this page!")
        get_db().delete_appointment_by_id(id)
        return jsonify(message="Appointment deleted successfully"), 204
