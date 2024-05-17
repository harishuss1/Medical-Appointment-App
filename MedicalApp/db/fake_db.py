import datetime 
import oracledb 
from MedicalApp.allergy import Allergy 
from MedicalApp.medical_room import MedicalRoom 
from ..user import User, MedicalPatient 
from oracledb import IntegrityError 
from ..appointments import Appointments
from MedicalApp.note import Note

class FakeDB:

    def __init__(self):
        self.allergies = [Allergy(1, "Peanuts", "Allergic reaction to peanuts causing hives and swelling."), Allergy(
            2, "Penicillin", "Allergic reaction to penicillin causing difficulty breathing and rash."), Allergy(3, "Blueberries", "Allergic reaction to blueberries causing hives and swelling.")]
        self.tokens = ["km9b5-UeGr3SDy6PszxFZRRvqiE",
                       "mIzbZLyEzNKW7SP5NAx9eUHUq_w", "tF1fG-t-R5hu3USXZcDIlKvIwXI", "ErU49l4Du_LEvsV1AgU9SIllZ1g", "2z12xfm3gqvZr1kZIAi4YXahpeA", "3e12xfm3gqvZr1kZIAi4YXahpaX"]
        self.patients = []
        #                                  weight, email,              password,                                                                                                                                                            first_name, last_name, access_level, dob,              blood_type, height, allergies=None, avatar_path=None, id=None
        self.patients.append(MedicalPatient(68.0, "maddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Maddie", "Buckley", "PATIENT", datetime.date(1985, 10, 5), "O-", 168.0, allergies=[self.allergies[0]], id=6, tokens=[self.tokens[0]]))
        self.patients.append(MedicalPatient(70.2, "chimney@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Howard", "Han", "PATIENT", datetime.date(1985, 10, 5), "A+", 168.0, id=7, tokens=[self.tokens[1]]))
        self.patients.append(MedicalPatient(75.2, "eddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68",
                             "Eddie", "Diaz", "PATIENT", datetime.date(1985, 10, 5), "B+", 170.0, id=8, tokens=[self.tokens[2]]))
        self.users = []
        self.users.append(User("maddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Maddie", "Buckley", "PATIENT", tokens=[self.tokens[0]], id=6))
        self.users.append(User("chimney@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Howard", "Han", "PATIENT", tokens=[self.tokens[1]], id=7))
        self.users.append(User("eddie@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Eddie", "Diaz", "PATIENT", tokens=[self.tokens[2]], id=8))
        self.users.append(User("bobby@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Bobby", "Nash", "STAFF", tokens=[self.tokens[3]], id=9))
        self.users.append(User("blocked@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "Blocked", "User", "BLOCKED", tokens=[self.tokens[4]], id=10))
        self.users.append(User("blocked@example.com", "scrypt:32768:8:1$FGTAHUp5LISWRIg8$7353fe1b7e4599016f3dfd29dc2f478bb00fbb1ca016572a3c84e82b8866c4785958b4933ed90dc2fd01f1a217478843aa634f3cab2e97f7b1eb2c4ac8540e68", "User", "User", "ADMIN_USER", tokens=[self.tokens[5]], id=11))
        self.appointments = [
             Appointments(
                patient=self.patients[0],
                doctor=self.users[3],
                appointment_time=datetime.datetime.now(),
                status=0,
                location=MedicalRoom("101", "Room 101"),
                description="Regular checkup",
                id=1
            ),
            Appointments(
                patient=self.patients[0],
                doctor=self.users[3],
                appointment_time=datetime.datetime.now(),
                status=0,
                location=MedicalRoom("102", "Room 102"),
                description="Dental appointment",
                id=2
            )
        ]
        self.rooms = [
            MedicalRoom("101", "Test1"),
            MedicalRoom("102", "Test2"),
            MedicalRoom("103", "Test3"),
            MedicalRoom("104", "Test4"),
            MedicalRoom("105", "Test5"),
        ]
        self.note = []
        self.note.append(Note(patient=self.patients[0], note_taker=self.users[3], note_date=datetime.date(2024,5,30), note='Follow-up examination conducted. Patient reports improvement in condition. Continuing current medication.', attachement_path=["/attachments/attachments1.pdf"],id=1))
        self.note.append(Note(patient=self.patients[1], note_taker=self.users[3], note_date=datetime.date(2024,6,7), note='Patient presented with symptoms of flu. Prescribed medication and advised bed rest.', attachement_path=["attachments.attachment2.pdf"],id=2))
        self.note.append(Note(patient=self.patients[1], note_taker=self.users[3], note_date=datetime.date(2024,8,21), note='Patient presented with symptoms of flu again. Medication does not work.', attachement_path=["attachments.attachment4.pdf"],id=3))

    def get_notes(self):
        return self.note
    
    def get_notes_page_number(self, page, patient_id=None, note_taker_id=None):
        if page is None:
            raise ValueError("Page number cannot be None")
        if patient_id is not None and not isinstance(patient_id, int):
            raise TypeError("Patient ID must be an integer")
        if note_taker_id is not None and not isinstance(note_taker_id, int):
            raise TypeError("Note taker ID must be an integer")

        try:
            page = int(page)
        except ValueError:
            raise TypeError("Page number must be an integer")

        notes = []
        offset = (page - 1) * 2
        count = 2
        if patient_id is not None or note_taker_id is not None:
            filtered_notes = [
                note for note in self.note
                if (patient_id is not None and note.patient.id == patient_id) or
                (note_taker_id is not None and note.note_taker.id == note_taker_id)
            ]
        else:
            filtered_notes = self.note

        end = min(count + offset, len(filtered_notes))

        for i in range(offset, end):
            notes.append(filtered_notes[i])

        return notes
    
    def get_note_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be None")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        for note in self.note:
            if (id == note.id):
                return note
        return None
    
    def create_note(self, note):
        if not isinstance(note, Note):
            raise TypeError("Invalid note type")
        note.id = len(self.note)+1
        self.note.append(note)
        return note.id
        
    def add_medical_room(self, room_number, description):
        if (room_number is None or description is None):
            raise ValueError("Parameters cannot be none")
        if room_number is not None and not isinstance(room_number, str) or description is not None and not isinstance(description, str) :
            raise TypeError("Parameters of incorrect type")
        for room in self.rooms:
            if room_number == room.room_number:
                raise IntegrityError()

        self.rooms.append(MedicalRoom(room_number, description))

    def get_user_by_token(self, token):
        if (not isinstance(token, str)):
            raise TypeError("Parameters of incorrect type")

        for user in self.users:
            if (token in user.tokens):
                return user
        return None
    
    def get_user_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be None")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        for user in self.users:
            if (id == user.id):
                return user
        return None

    def get_appointment_by_id(self, appointment_id):
        if (appointment_id is None):
            raise ValueError("Parameters cannot be None")
        try:
            appointment_id = int(appointment_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        for appointment in self.appointments:
            if appointment.id == appointment_id:
                return appointment
        return None

    def get_appointments(self):
        return self.appointments

    def add_appointment(self, appointment):
        if not isinstance(appointment, Appointments):
            raise TypeError("Invalid appointment type")
        appointment.id = len(self.appointments) + 1
        self.appointments.append(appointment)
        return appointment.id
        

    def update_appointment(self, appointment):
        for a in self.appointments:
            if appointment.id == a.id:
                self.appointments.remove(a)
                self.appointments.append(appointment)

    def get_appointments_page_number(self, page, doctor_first_name, doctor_last_name, patient_first_name, patient_last_name):
        if page is None: 
            raise ValueError("Page parameter cannot be None or empty")
        
        appointments = []
        for appointment in self.appointments:
            if (doctor_first_name is None or doctor_first_name == appointment.doctor.first_name) and \
            (doctor_last_name is None or doctor_last_name == appointment.doctor.last_name) and \
            (patient_first_name is None or patient_first_name == appointment.patient.first_name) and \
            (patient_last_name is None or patient_last_name == appointment.patient.last_name):
                appointments.append(appointment)
        start_index = (page - 1) * 20
        end_index = start_index + 20
        return appointments[start_index:end_index]

    def delete_appointment_by_id(self, appointment_id):
        appointment= self.get_appointment_by_id(appointment_id)    
        self.appointments.remove(appointment)

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

    def get_all_allergies(self):
        return self.allergies

    def get_patients(self):
        return self.patients

    def get_patient_allergies(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")

        patient = self.get_patients_by_id(patient_id)
        return patient.allergies
    
    def get_allergy_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be None")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        allergy = None
        for a in self.allergies:
            if a.id == id:
                allergy = a
        return allergy
    
    def update_allergies(self, patient_id, allergy_ids):
        if (patient_id is None or allergy_ids is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
            for allergy in allergy_ids:
                int(allergy)
        except:
            raise TypeError("Parameters of incorrect type")
        
        new_allergies = []
        
        for id in allergy_ids:
            allergy = self.get_allergy_by_id(id)
            if allergy is None:
                raise oracledb.IntegrityError()
            new_allergies.append(allergy)
        
        patient = self.get_patients_by_id(patient_id)
        patient.allergies = new_allergies

    def get_allergies_page_number(self, page, name):
        if (page is None):
            raise ValueError("Parameters cannot be none")
        if (name is not None and not isinstance(name, str)):
            raise TypeError("Parameters of incorrect type")

        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")

        allergies = []
        offset = ((page - 1)*2)
        count = 2
        
        end = count+offset if count+offset <= len(self.allergies) else len(self.allergies)

        for i in range(offset, end):
            allergy = self.allergies[i]
            if name is None:
                allergies.append(allergy)
            if name is not None and allergy.name == name:
                allergies.append(allergy)
        return allergies
    
    def get_patients_page_number(self, page, first_name, last_name):
        if (page is None):
            raise ValueError("Parameters cannot be none")
        if (first_name is not None and not isinstance(first_name, str) or last_name is not None and not isinstance(last_name, str)):
            raise TypeError("Parameters of incorrect type")

        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")

        patients = []
        offset = ((page - 1)*2)
        count = 2
        
        end = count+offset if count+offset <= len(self.patients) else len(self.patients)

        for i in range(offset, end):
            patient = self.patients[i]
            if first_name is None and last_name is None:
                patients.append(patient)
            if first_name is not None and patient.first_name == first_name:
                patients.append(patient)
            if last_name is not None and patient.last_name == last_name:
                patients.append(patient)
        return patients

    def get_patients_by_id(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")

        patient = None
        for p in self.patients:
            if p.id == patient_id:
                patient = p
        return patient
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


    def get_doctors(self):
        doctors = [user for user in self.users if user.access_level in [
            'STAFF', 'ADMIN']]
        return doctors

    def get_doctor_by_id(self, id):
        if id is None:
            raise ValueError("ID cannot be none")

        for doctor in self.users:
            if doctor.id == id:
                return doctor
        return None

    def get_doctors_page_number(self, page, first_name, last_name):
        if page is None:
            raise ValueError("Parameters cannot be none")
        if (first_name is not None and not isinstance(first_name, str)) or (last_name is not None and not isinstance(last_name, str)):
            raise TypeError("Parameters of incorrect type")

        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")
        
        doctors = self.get_doctors()
        offset = ((page - 1)*2)
        count = 2
        
        results = []
        
        end = count+offset if count+offset <= len(doctors) else len(doctors)

        for i in range(offset, end):
            doctor = doctors[i]
            if first_name is None and last_name is None:
                results.append(doctor)
            if first_name is not None and doctor.first_name == first_name:
                results.append(doctor)
            if last_name is not None and doctor.last_name == last_name:
                results.append(doctor)
        return results

    def run_file(self, file_path):
        pass

    def close(self):
        pass
