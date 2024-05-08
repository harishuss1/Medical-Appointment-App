from flask import Blueprint, abort, jsonify, request
from MedicalApp.db.dbmanager import get_db
from MedicalApp.appointments import Appointments

bp = Blueprint('appointments_api', __name__, url_prefix='/api/appointments/')


@bp.route('', methods=['GET', 'POST'])
def get_appointments():
    if request.method == 'POST':
        data = request.json
        appointment = Appointments.from_json(data)
        get_db().add_appointment(appointment)

    if request.args:
        id = request.args.get("id")
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
