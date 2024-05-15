from flask import Blueprint, Response, abort, jsonify, request
from flask_login import current_user
from MedicalApp.db.dbmanager import get_db
from MedicalApp.appointments import Appointments

bp = Blueprint('appointments_api', __name__, url_prefix='/api/appointments/')


@bp.route('', methods=['GET', 'POST'])
def get_appointments_api():
    if request.method == 'POST':
        appointment = Appointments.from_json(request.json)
        get_db().add_appointment(appointment)

    if request.args:
        page = int(request.args.get("page"))
        id = request.args.get("id")

        if page is None or not isinstance(page, int):
            page = 1

        if id:
            appointment = get_db().get_appointment_by_id(id)
            if appointment:
                return jsonify(appointment.__dict__)
            else:
                abort(404)
        else:
            abort(400)

    appointments = get_db().get_appointments()
    json_appointments = [x.__dict__ for x in appointments]
    return jsonify(json_appointments)


@bp.route('/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def get_appointment_by_id_api(id):
    if request.method == 'GET':
        try:
            appointment = get_db().get_appointment_by_id(id)
            return jsonify(appointment.to_json())
        except Exception:
            abort(500)
    
    elif request.method == 'PUT':
        appointment_json = request.json
        if appointment_json:
            appointment = Appointments.from_json(appointment_json)
            try:
                target_appointment = get_db().get_appointment_by_id(appointment.id)
                if target_appointment.id != appointment.id:
                    abort(500)
                
                # Check if the current user is a patient or a doctor
                if current_user.access_level == 'PATIENT':
                    # Patient can only update appointment_time and description
                    if hasattr(appointment.doctor, 'first_name'):
                        target_appointment.doctor.first_name = appointment.doctor.first_name
                    if hasattr(appointment.doctor, 'last_name'):
                        target_appointment.doctor.last_name = appointment.doctor.last_name
                    target_appointment.appointment_time = appointment.appointment_time
                    target_appointment.description = appointment.description
                elif current_user.access_level == 'STAFF':
                    # Doctor can only update status and location
                    target_appointment.status = appointment.status
                    target_appointment.location = appointment.location
                
                get_db().update_appointment(target_appointment)
                return jsonify(message="Appointment updated successfully"), 200
            except Exception:
                abort(500)
        else:
            abort(400)
    
    elif request.method == 'DELETE':
        try:
            get_db().delete_appointment_by_id(id)
            return jsonify(message="Appointment deleted successfully"), 200
        except Exception:
            abort(500)

