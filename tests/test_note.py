import unittest
from MedicalApp import create_app
from datetime import date
from MedicalApp.note import Note
from MedicalApp.user import MedicalPatient, User


class NoteTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
    
    def test_create_note_successful(self):
        patient = MedicalPatient(weight=70.0, email="patient@example.com", password="password",
                                 first_name="John", last_name="Doe", access_level="PATIENT",
                                 dob=date(1990, 1, 1), blood_type="O+", height=175.0,
                                 avatar_path="/avatars/patient.jpg", id=123)
        note_taker = User(email="doctor@example.com", password="password",
                          first_name="Dr. Jane", last_name="Smith", access_level="STAFF",
                          avatar_path="/avatars/doctor.jpg", id=456)
        note_date = date(2024, 5, 30)
        note_text = "This is a new note."
        attachment_paths = ["/attachments/attachment1.pdf", "/attachments/attachment2.jpg"]

        note = Note(patient=patient, note_taker=note_taker, note_date=note_date,
                    note=note_text, attachement_path=attachment_paths, id=789)

        self.assertEqual(patient, note.patient)
        self.assertEqual(note_taker, note.note_taker)
        self.assertEqual(note_date, note.note_date)
        self.assertEqual(note_text, note.note)
        self.assertEqual(attachment_paths, note.attachement_path)
        self.assertEqual(789, note.id)

    def test_create_note_bad_patient(self):
        with self.assertRaises(TypeError):
            Note(patient="invalid_patient", note_taker=None, note_date=None, note=None)
    
    def test_create_note_bad_note_taker(self):
        with self.assertRaises(TypeError):
            Note(patient=None, note_taker="invalid_note_taker", note_date=None, note=None)

    def test_create_note_bad_note_date(self):
        with self.assertRaises(TypeError):
            Note(patient=None, note_taker=None, note_date="invalid_note_date", note=None)

    def test_create_note_bad_note_text(self):
        with self.assertRaises(TypeError):
            Note(patient=None, note_taker=None, note_date=None, note=123)

    def test_create_note_bad_attachment_paths(self):
        with self.assertRaises(TypeError):
            Note(patient=None, note_taker=None, note_date=None, note=None, attachement_path="invalid_attachment_paths")

    def test_create_note_no_attachment_paths(self):
        # Test creating a note without attachment paths
        patient = MedicalPatient(weight=70.0, email="patient@example.com", password="password",
                                first_name="John", last_name="Doe", access_level="PATIENT",
                                dob=date(1990, 1, 1), blood_type="O+", height=175.0,
                                avatar_path="/avatars/patient.jpg", id=123)
        note_taker = User(email="doctor@example.com", password="password",
                        first_name="Dr. Jane", last_name="Smith", access_level="STAFF",
                        avatar_path="/avatars/doctor.jpg", id=456)
        note_date = date(2024, 5, 30)
        note_text = "This is a new note."

        note = Note(patient=patient, note_taker=note_taker, note_date=note_date,
                    note=note_text, id=789)

        self.assertEqual(patient, note.patient)
        self.assertEqual(note_taker, note.note_taker)
        self.assertEqual(note_date, note.note_date)
        self.assertEqual(note_text, note.note)
        self.assertEqual([], note.attachement_path)
        self.assertEqual(789, note.id)

    if __name__ == '__main__':
        unittest.main()