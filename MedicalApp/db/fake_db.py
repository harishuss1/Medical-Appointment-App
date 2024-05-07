from ..user import User, MedicalPatient
from oracledb import IntegrityError
from appointments import Appointments



class FakeDB:

    def __init__(self):
        self.users = []
        self.appointments = []

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


    def run_file(self, file_path):
        pass

    def close(self):
        pass
