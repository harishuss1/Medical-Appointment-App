from flask import Blueprint, jsonify, request
from MedicalApp.db.dbmanager import get_db
from MedicalApp.note import Note

bp = Blueprint('note_api', __name__, url_prefix='/api/notes')

@bp.route('', methods=['GET'])
def get_notes_by_patient():
     try:
         patient_id = request.args.get('patient_id')

         if patient_id is None:
             return jsonify({'error': 'Patient ID is required'}), 400
         patient_id = int(patient_id)

         notes = get_db().get_notes_by_patient_id(patient_id)
         return jsonify([note.serialize() for note in notes])
     except Exception as e:
         return jsonify({'error': str(e)}), 500
