from .user import MedicalPatient, User 

class Note:
    def __init__(self, id, patient, note_taker, note_date, note, attachement_path):
        if not isinstance(id, int):
            raise TypeError("Illegal type for id")
        if not isinstance(patient, MedicalPatient):
            raise TypeError("Illegal type for patient")
        if not isinstance(note_taker, User):
            raise TypeError("Illegal type for note taker")
        if note_taker.access_level != 'STAFF':
            raise TypeError("Notes can only be taken by doctors")
        if not isinstance(note_date, str):
            raise TypeError("Illegal type for note date")
        if not isinstance(note, str):
            raise TypeError("Illegal type for note")
        if not isinstance(attachement_path, str):
            raise TypeError("Illegal type for attachement_path")

        self.id = id
        self.patient = patient
        self.note_taker = note_taker
        self.note = note
        self.attachement_path = attachement_path
