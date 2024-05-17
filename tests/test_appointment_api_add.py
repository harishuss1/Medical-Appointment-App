import json
import unittest
import datetime

from flask import jsonify
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
from MedicalApp.db.fake_db import FakeDB
from MedicalApp.user import User, MedicalPatient
from MedicalApp.medical_room import MedicalRoom

class AppointmentsUpdateTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app(test_config={})
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_get_appointment_by_id_success_200(self):
        # Mock the database object
        fake_db = FakeDB()

        # Create sample patient, doctor, and room
        patient = MedicalPatient(
            weight=70.5,  # example weight in kg
            email='john.doe@example.com',
            password='password123',
            first_name='John',
            last_name='Doe',
            access_level='PATIENT',
            dob=datetime.date(1990, 1, 1),
            blood_type='O+',
            height=175.0,  # example height in cm
            allergies=[],
            id=1
        )

        doctor = User(
            email='dr.smith@example.com',
            password='password123',
            first_name='Dr. Smith',
            last_name='Smith',
            access_level='DOCTOR',
            id=2
        )

        room = MedicalRoom(room_number='101', description='Room 101')

        # Add them to the fake database
        fake_db.add_patient(patient)
        fake_db.add_user(doctor)
        fake_db.add_room(room)

        # Add a sample appointment to the fake database
        appointment_id = 1
        appointment = Appointments(
            id=appointment_id,
            patient_id=patient.id,
            doctor_id=doctor.id,
            appointment_time=datetime.datetime.now() + datetime.timedelta(days=1),
            location=room.room_number,
            description='Regular checkup'
        )
        fake_db.add_appointment(appointment)

        response = self.client.get(f'/api/appointments/{appointment_id}')

        self.assertEqual(response.status_code, 200)

        expected_appointment = fake_db.get_appointment_by_id(appointment_id)
        self.assertEqual(response.json, jsonify(expected_appointment.to_dict()).json)

if __name__ == '__main__':
    unittest.main()
