class Appointments:
    def __init__(self, id, patient_id, doctor_id, appointment_time, status, location, description):
        if not isinstance(id, int) or id < 0:
            raise ValueError('Illegal type for patient id')
        self.id = id
        
        if not isinstance(patient_id, int) or patient_id < 0:
            raise ValueError('Illegal type for patient id')
        self.patient_id = patient_id

        if not isinstance(doctor_id, int) or doctor_id < 0:
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
        self.description = description

    def __str__(self):
        return f'{self.id} {self.patient_id} {self.doctor_id} {self.appointment_time} {self.status} {self.location} {self.description}'