import datetime
import json
from MedicalApp.medical_room import MedicalRoom
from MedicalApp.user import User, MedicalPatient


class Appointments:
    def from_json(data):
        if not isinstance(data, dict):
            raise TypeError("Data must be a dictionary")

        patient_data = data['patient']
        doctor_data = data['doctor']

        if not isinstance(patient_data, dict):
            raise ValueError("Patient data must be a dictionary")

        if not isinstance(doctor_data, dict):
            raise ValueError("Doctor data must be a dictionary")

        patient = MedicalPatient.from_json(patient_data)
        doctor = User.from_json(doctor_data)

        appointment_time = str(data['appointment_time'])
        status = data['status']
        location = data['location']
        description = data['description']

        return Appointments(data['id'], patient, doctor, appointment_time, status, location, description)

    def to_json(self):
            data = {}
            data['id']= str(self.id),
            data['patient']= str(self.patient.to_json()),
            #data['doctor']: str(self.doctor.to_json()),
            data['appointment_time']= str(self.appointment_time),
            data['status']= str(self.status),
            data['location']= str(self.location.to_json()),
            data['description']= str(self.description)
            return data
    
    def __init__(self, patient, doctor, appointment_time, status, location, description, id=None):
        if id != None and not isinstance(id, int):
            raise ValueError('Illegal type for patient id')
        self.id = id

        if not isinstance(patient, MedicalPatient):
            raise ValueError('Illegal type for patients objects')
        self.patient = patient

        if not isinstance(doctor, User):
            raise ValueError('Illegal type for doctor objects')
        self.doctor = doctor

        if not isinstance(appointment_time, datetime.date):
            raise ValueError('Illegal type for appointment_time')
        self.appointment_time = appointment_time

        if not isinstance(status, int) or status not in [-1, 0, 1]:
            raise ValueError('Illegal value for status')
        self.status = status

        if not isinstance(location, MedicalRoom):
            raise ValueError('Illegal type for location')
        self.location = location

        if not isinstance(description, str):
            raise ValueError('Illegal type for description')
        self.description = description

    def __str__(self):
        return f'{self.id} {self.patient} {self.doctor} {self.appointment_time} {self.status} {self.location} {self.description}'
