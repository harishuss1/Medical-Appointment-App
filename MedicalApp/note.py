import datetime
from .user import MedicalPatient, User


class Note:
    def __init__(self, patient, note_taker, note_date, note, attachement_path=[], id=None):
        if id != None and not isinstance(id, int):
            raise TypeError("Illegal type for id")
        if not isinstance(patient, MedicalPatient):
            raise TypeError("Illegal type for patient")
        if not isinstance(note_taker, User):
            raise TypeError("Illegal type for note taker")
        if note_taker.access_level != 'STAFF':
            raise TypeError("Notes can only be taken by doctors")
        if not isinstance(note_date, datetime.date):
            raise TypeError("Illegal type for note date")
        if not isinstance(note, str):
            raise TypeError("Illegal type for note")
        if attachement_path != None and not isinstance(attachement_path, list):
            raise TypeError("Illegal type for attachement_path")

        self.id = id
        self.patient = patient
        self.note_taker = note_taker
        self.note_date = note_date
        self.note = note
        self.attachement_path = attachement_path

    def serialize(self):
        return {
            'id': self.id,
            'patient': self.patient.serialize(),
            'note_taker': self.note_taker.serialize(),
            'note_date': self.note_date.strftime('%Y-%m-%d'),
            'note': self.note,
            'attachement_path': self.attachement_path
        }

    @staticmethod
    def from_json(data):
        # Validate required fields
        required_fields = ['patient_id', 'note_taker_id', 'note_date', 'note']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        # Extract data
        patient = MedicalPatient(data['patient_id'])
        note_taker = User(data['note_taker_id'])
        note_date = datetime.datetime.strptime(data['note_date'], '%Y-%m-%d').date()
        note = data['note']
        attachement_path = data.get('attachement_path', [])

        return Note(patient, note_taker, note_date, note, attachement_path)


    def update_from_json(self, data):
        # Update note attributes from JSON data
        if 'note_date' in data:
            self.note_date = datetime.datetime.strptime(data['note_date'], '%Y-%m-%d').date()
        if 'note' in data:
            self.note = data['note']
        if 'attachement_path' in data:
            self.attachement_path = data.get('attachement_path', [])
