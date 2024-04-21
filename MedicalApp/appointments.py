class Appointments:
    def __init__(self, patient_id, doctor_id, appointment_time, status, location, description, id):
        if not isinstance(patient_id, int) or id < 0:
            raise ValueError('Illegal type for patient id')
        self.patient_id = patient_id

        if not isinstance(doctor_id, int) or id < 0:
            raise ValueError('Id must be positive or Illegal type for doctor id')
        self.doctor_id = doctor_id

        if not isinstance(appointment_time, str):
            raise ValueError('Illegal type for appointment_time')
        self.appointment_time = appointment_time

        if not isinstance(status, int):
            raise ValueError('Illegal type for status')
        self.status = status

        if not isinstance(location, str):
            raise ValueError('Illegal type for location')
        self.location = location

        if not isinstance(description, str):
            raise ValueError('Illegal type for description')
        self.location = description

        