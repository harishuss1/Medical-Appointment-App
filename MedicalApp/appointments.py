import json
from MedicalApp.user import User,MedicalPatient


class Appointments:
    def from_json(data):
        if not isinstance(data, dict):
            raise TypeError()
        return Appointments(data['id'], data['patient_id'], data['doctor_id'], data['appointment_time'],
                            data['status'], data['location'], data['description'])

    def to_json(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'appointment_time': self.appointment_time,
            'status': self.status,
            'location': self.location,
            'description': self.description
        }

    def __init__(self, id, patients, doctors, appointment_time, status, location, description):
        if not isinstance(id, int) or id < 0:
            raise ValueError('Illegal type for patient id')
        self.id = id

        if not isinstance(patients, MedicalPatient):
            raise ValueError('Illegal type for patients objects')
        self.patients = patients

        if not isinstance(doctors, User):
            raise ValueError('Illegal type for doctor objects')
        self.doctors = doctors

        if not isinstance(appointment_time, str):
            raise ValueError('Illegal type for appointment_time')
        self.appointment_time = appointment_time

        if not isinstance(status, int or status > 1 or status < -1):
            raise ValueError('Illegal type for status')
        self.status = status

        if not isinstance(location, str):
            raise ValueError('Illegal type for location')
        self.location = location

        if not isinstance(description, str):
            raise ValueError('Illegal type for description')
        self.description = description

    def __str__(self):
        return f'{self.id} {self.patients} {self.doctors} {self.appointment_time} {self.status} {self.location} {self.description}'
