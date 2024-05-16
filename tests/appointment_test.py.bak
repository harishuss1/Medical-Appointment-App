import unittest
import datetime
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
from MedicalApp.user import User, MedicalPatient
from MedicalApp.medical_room import MedicalRoom

class AppointmentsTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app(test_config={})
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_create_appointment_successful(self):
        patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", datetime.date(2001, 1, 1), "A+", 170.0, access_level="PATIENT")
        doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
        room = MedicalRoom("101", "Room 101")
        appointment_time = datetime.datetime.now()
        appointment = Appointments(patient, doctor, appointment_time, 0, room, "Regular checkup", 1)
        self.assertEqual(patient, appointment.patient)
        self.assertEqual(doctor, appointment.doctor)
        self.assertEqual(appointment_time, appointment.appointment_time)
        self.assertEqual(0, appointment.status)
        self.assertEqual(room, appointment.location)
        self.assertEqual("Regular checkup", appointment.description)
        self.assertEqual(1, appointment.id)


    def test_create_appointment_bad_patient(self):
        with self.assertRaises(ValueError):
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            room = MedicalRoom("101", "Room 101")
            appointment_time = datetime.datetime.now()
            Appointments("patient", doctor, appointment_time, 0, room, "Regular checkup", 1)

    def test_create_appointment_bad_doctor(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            room = MedicalRoom("101", "Room 101")
            appointment_time = datetime.datetime.now()
            Appointments(patient, "doctor", appointment_time, 0, room, "Regular checkup", 1)

    def test_create_appointment_bad_appointment_time(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            room = MedicalRoom("101", "Room 101")
            Appointments(patient, doctor, "invalid_date", 0, room, "Regular checkup", 1)

    def test_create_appointment_bad_status(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            room = MedicalRoom("101", "Room 101")
            appointment_time = datetime.datetime.now()
            Appointments(patient, doctor, appointment_time, "invalid_status", room, "Regular checkup", 1)

    def test_create_appointment_bad_location(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            appointment_time = datetime.datetime.now()
            Appointments(patient, doctor, appointment_time, 0, "Room 101", "Regular checkup", 1)

    def test_create_appointment_bad_description(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            room = MedicalRoom("101", "Room 101")
            appointment_time = datetime.datetime.now()
            Appointments(patient, doctor, appointment_time, 0, room, 123, 1)

    def test_create_appointment_bad_id(self):
        with self.assertRaises(ValueError):
            patient = MedicalPatient(70.0, "patient@example.com", "test1", "Patient", "PATIENT", datetime.date(2001, 1, 1), "A+", 170.0, 170.0)
            doctor = User("doctor@doctor.com", "password", "Dr. Smith", "Smith", "STAFF")
            room = MedicalRoom("101", "Room 101")
            appointment_time = datetime.datetime.now()
            Appointments(patient, doctor, appointment_time, 0, room, "Regular checkup", "1")

if __name__ == '__main__':
    unittest.main()
