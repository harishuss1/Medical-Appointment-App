import datetime
from MedicalApp.appointments_views import update_appointment
from MedicalApp.medical_room import MedicalRoom
from ..user import User, MedicalPatient
from oracledb import IntegrityError
from ..appointments import Appointments



class FakeDB:

    def __init__(self):
        self.users = []
        self.appointments = [
             Appointments(
                patient=MedicalPatient("test1"),
                doctor=User("test1d"),
                appointment_time=datetime.datetime.now(),
                status=0,
                location=MedicalRoom("101", "Room 101"),
                description="Regular checkup"
            ),
            Appointments(
                patient=MedicalPatient("test2"),
                doctor=User("test2d"),
                appointment_time=datetime.datetime.now(),
                status=0,
                location=MedicalRoom("102", "Room 102"),
                description="Dental appointment"
            )
        ]
        self.rooms = [
            MedicalRoom("101", "Test1"),
            MedicalRoom("102", "Test2"),
            MedicalRoom("103", "Test3"),
            MedicalRoom("104", "Test4"),
            MedicalRoom("105", "Test5"),
        ]

    def get_appointment_by_id(self, appointment_id):
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    def get_appointments(self):
        return self.appointments

    def add_appointment(self, appointment):
        if not isinstance(appointment, Appointments):
            raise TypeError("Invalid appointment type")
        self.appointments.append(appointment)

    def update_appointment(self, appointment):
        updated_appointments = [
            appointment if appt.id == appointment.id else appt
            for appt in self.appointments
        ]
        if len(updated_appointments) == len(self.appointments):
            raise ValueError("Appointment not found")
        self.appointments = updated_appointments

    def delete_appointment_by_id(self, appointment_id):
        self.appointments = [
            appointment for appointment in self.appointments if appointment.id != appointment_id
        ]
        if len(self.appointments) == len(update_appointment):
            raise ValueError("Appointment not found")

    def get_medical_rooms(self):
        return self.rooms

    def get_medical_room_by_room_number(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None

    def get_medical_room_page_number(self, page, room_number):
        if room_number:
            return [room for room in self.rooms if room.room_number == room_number]
        else:
            start_index = (page - 1) * 20
            end_index = min(start_index + 20, len(self.rooms))
            return self.rooms[start_index:end_index]


    def run_file(self, file_path):
        pass

    def close(self):
        pass
