from flask import Blueprint, abort, jsonify, request
from flask_login import current_user
from MedicalApp.db.dbmanager import get_db
from MedicalApp.appointments import Appointments

bp = Blueprint('appointments_api', __name__, url_prefix='/api/appointments/')


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
def get_appointment_by_id_api(id):
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
        appointment_json = request.json
        if appointment_json:
            appointment = Appointments.from_json(appointment_json)
            try:
                target_appointment = get_db().get_appointment_by_id(appointment.id)
                if target_appointment.id != appointment.id:
                    abort(500)
                
                if current_user.access_level == 'PATIENT':
                    doctor_id = appointment_json.get('doctor.id')

                    if doctor_id is None:
                        abort(400, jsonify(message="Doctor ID is required for update"))

                    doctor = get_db().get_doctor_by_id(doctor_id)

                    if doctor is None:
                        abort(404, jsonify(message=f"Doctor with ID {doctor_id} not found"))
                    
                    target_appointment.doctor = doctor
                    target_appointment.appointment_time = appointment.appointment_time
                    target_appointment.description = appointment.description
                elif current_user.access_level == 'STAFF':
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
