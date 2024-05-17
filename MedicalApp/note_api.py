from flask import Blueprint, jsonify, make_response, request, abort, url_for
from .db.dbmanager import get_db
from oracledb import DatabaseError
from MedicalApp.note import Note
import urllib.parse

bp = Blueprint('note_api', __name__, url_prefix='/api/notes/')

@bp.route('', methods=['GET'])
def get_notes():
    notes = []
    page = 1
    patient_id = None
    note_taker_id = None
    
    if request.args:
        page = request.args.get("page", 1)
        try:
            page = int(page)
        except ValueError:
            abort(make_response(jsonify(id="400", description="The page number is of incorrect type"), 400))
        
        patient_id = request.args.get("patient_id")
        note_taker_id = request.args.get("note_taker_id")

        try:
            if patient_id is not None:
                patient_id = int(patient_id)
            if note_taker_id is not None:
                note_taker_id = int(note_taker_id)
        except ValueError:
            abort(make_response(jsonify(id="400", description="Patient ID and note taker ID must be integers"), 400))
        
        try:
            notes = get_db().get_notes_page_number(page, patient_id, note_taker_id)
        except DatabaseError:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))
        except TypeError:
            abort(make_response(jsonify(id="400", description="The data sent is of incorrect type"), 400))
        except ValueError:
            abort(make_response(jsonify(id="400", description="The data sent cannot be empty"), 400))
    else:
        try:
            notes = get_db().get_notes_page_number(page, None, None)
        except DatabaseError:
            abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))

    if not notes:
        abort(make_response(jsonify(id="404", description="No notes currently available in the database"), 404))

    data = {}
    try:
        count = len(get_db().get_notes(patient_id)) if patient_id else len(get_db().get_notes_page_number(page, None, None))
    except DatabaseError:
        abort(make_response(jsonify(id="409", description='Something went wrong with our database'), 409))

    data['count'] = count
    data['previous'] = urllib.parse.urljoin(request.url_root, url_for('note_api.get_notes', page=(page-1))) if page > 1 else ""
    data['next'] = urllib.parse.urljoin(request.url_root, url_for('note_api.get_notes', page=(page+1))) if len(notes) == 20 else ""
    data['results'] = [note.to_json(request.url_root) for note in notes]

    return jsonify(data)