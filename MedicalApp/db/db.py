from datetime import date
import datetime
import oracledb
import os
from flask import g

from MedicalApp.allergy import Allergy
from MedicalApp.medical_room import MedicalRoom
from ..appointments import Appointments
from ..user import MedicalPatient
from ..note import Note
from werkzeug.security import generate_password_hash

from MedicalApp.user import User
from MedicalApp.appointments import Appointments


class Database:
    def __init__(self, autocommit=True):
        self.__connection = oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                             host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")
        self.__connection.autocommit = autocommit

    def run_file(self, file_path):
        statement_parts = []
        with self.__connection.cursor() as cursor:
            with open(file_path, 'r') as f:
                for line in f:
                    statement_parts.append(line)
                    if line.strip('\n').strip('\n\r').strip().endswith(';'):
                        statement = "".join(
                            statement_parts).strip().rstrip(';')
                        if statement:
                            try:
                                cursor.execute(statement)
                            except Exception as e:
                                print(e)
                        statement_parts = []

    def delete_user(self, user_email):
        if (user_email is None):
            raise ValueError("Parameters cannot be none")
        if (not isinstance(user_email, str)):
            raise TypeError("Parameters of incorrect type")
        
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM medical_users WHERE email = :email",
                    {'email': user_email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error deleting user:", e)
            raise

    def block_user(self, email):
        if (email is None):
            raise ValueError("Parameters cannot be none")
        if (not isinstance(email, str)):
            raise TypeError("Parameters of incorrect type")
        
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE medical_users SET user_type = 'BLOCKED' WHERE email = :email",
                    {'email': email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error blocking user:", e)
            raise

    def change_user_type(self, user_email, new_user_type):
        if (user_email is None or new_user_type is None):
            raise ValueError("Parameters cannot be none")
        if (not isinstance(user_email, str) or not isinstance(new_user_type, str)):
            raise TypeError("Parameters of incorrect type")
        
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE medical_users SET user_type = :user_type WHERE email = :email",
                    {'user_type': new_user_type, 'email': user_email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error changing user type:", e)
            raise

    # status 0 = pending, status 1 = confirmed, status -1 = cancel

    def get_appointments_by_status_doctor(self, status, doctor_id):
        if (status is None or doctor_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            status = int(status)
            doctor_id = int(doctor_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        status = int(status)
        doctor_id = int(doctor_id)
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id INNER JOIN MEDICAL_ROOMS mr ON app.location = mr.room_number WHERE app.status = :status AND app.doctor_id = :doctor_id ',
                status=status, doctor_id=doctor_id)
            for row in results:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                location = MedicalRoom(row[25], row[26])
                appointments.append(Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0]))
        return appointments

    def get_patients(self):
        patients = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT 
                mp.WEIGHT, p.id, p.AVATAR_PATH, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, 
                mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT
                FROM medical_users p INNER JOIN MEDICAL_PATIENTS mp 
                ON(p.id = mp.id)
                """)
            for row in results:
                patients.append(MedicalPatient(float(row[0]), row[3], row[4], row[5], row[6], row[7], row[8], row[9], float(
                    row[10]), avatar_path=row[2], id=int(row[1])))
        return patients
    
    def get_allergies_page_number(self, page, name): #TEST!
        if (page is None):
            raise ValueError("Parameters cannot be none")
        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")
        
        if (name is not None and not isinstance(name, str)):
            raise TypeError("Parameters of incorrect type")
        
        allergies = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                f"""
                SELECT 
                a.id, a.name, a.description
                FROM medical_allergies a
                WHERE
                { "name = :name" if name is not None and name != '' else ":name != name"}
                OFFSET :offset ROWS
                FETCH NEXT :count ROWS ONLY
                """,
                offset=((page - 1)*10),
                count=10,
                name=str(name)) #str of None is an empty string! therefore :name != '' will always be true
            for row in results:
                allergies.append(Allergy(int(row[0]), str(row[1]), str(row[2])))
        return allergies
    
    def get_patients_page_number(self, page, first_name, last_name): #TEST!
        if (page is None):
            raise ValueError("Parameters cannot be none")
        if (first_name is not None and not isinstance(first_name, str) or last_name is not None and not isinstance(last_name, str)):
            raise TypeError("Parameters of incorrect type")
        
        try:
            page = int(page)
        except:
            raise TypeError("Parameters of incorrect type")
        
        patients = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                f"""
                SELECT 
                mp.WEIGHT, p.id, p.AVATAR_PATH, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, 
                mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT
                FROM medical_users p INNER JOIN MEDICAL_PATIENTS mp 
                ON(p.id = mp.id)
                WHERE
                { "first_name = :first_name" if first_name is not None and first_name != '' else ":first_name != first_name"} OR
                { "last_name = :last_name" if last_name is not None and last_name != '' else ":last_name != last_name"}
                OFFSET :offset ROWS
                FETCH NEXT :count ROWS ONLY
                """,
                offset=((page - 1)*10),
                count=10,
                first_name=str(first_name),
                last_name=str(last_name))
            for row in results:
                allergies = self.get_patient_allergies(int(row[1]))
                patients.append(MedicalPatient(float(row[0]), row[3], row[4], row[5], row[6], row[7], row[8], row[9], float(
                    row[10]), allergies=allergies, avatar_path=row[2], id=int(row[1])))
        return patients
    
    def get_doctors(self):
        doctors = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT 
                u.id, u.AVATAR_PATH, u.EMAIL, u.PASSWORD, u.FIRST_NAME, u.LAST_NAME, u.USER_TYPE
                FROM medical_users u
                WHERE u.user_type = 'STAFF' OR u.user_type = 'ADMIN'
                """)
            for row in results:
                doctors.append(User(row[2], row[3], row[4], row[5], row[6], 
                avatar_path=row[1], id=int(row[0])))
        return doctors
    
    def get_doctors_page_number(self, page, first_name, last_name):
        if (page is None):
            raise ValueError("Parameters cannot be none")
        
        doctors = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                f"""
                SELECT 
                u.id, u.AVATAR_PATH, u.EMAIL, u.PASSWORD, u.FIRST_NAME, u.LAST_NAME, u.USER_TYPE
                FROM medical_users u
                WHERE
                u.USER_TYPE = 'DOCTOR' AND
                ({ "first_name = :first_name" if first_name is not None and first_name != '' else ":first_name != :first_name"} OR
                { "last_name = :last_name" if last_name is not None and last_name != '' else ":last_name != :last_name"})
                OFFSET :offset ROWS
                FETCH NEXT :count ROWS ONLY
                """,
                offset=((page - 1)*20),
                count=20,
                first_name=first_name,
                last_name=last_name)
            for row in results:
                doctors.append(User(row[2], row[3], row[4], row[5], row[6], avatar_path=row[1], id=int(row[0])))
        return doctors

    def get_doctors_by_id(self, id):
        if (id is None):
            raise ValueError("ID cannot be none")
        
        doctor = None
        with self.__get_cursor() as cursor:
            result = cursor.execute(
                f"""
                SELECT 
                u.id, u.AVATAR_PATH, u.EMAIL, u.PASSWORD, u.FIRST_NAME, u.LAST_NAME, u.USER_TYPE
                FROM medical_users u
                WHERE
                u.USER_TYPE = 'DOCTOR' AND
                u.id = :id
                """,
                id=id)
            row = result.fetchone()
            if row is not None:
                doctor = User(row[2], row[3], row[4], row[5], row[6], avatar_path=row[1], id=int(row[0]))
        return doctor
    
    def get_appointments_by_status_patient(self, status, patient_id): #TEST!
        if (status is None or patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            status = int(status)
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        status = int(status)
        patient_id = int(patient_id)
        
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id INNER JOIN MEDICAL_ROOMS mr ON app.location = mr.room_number WHERE app.status = :status AND app.patient_id = :patient_id',
                status=status, patient_id=patient_id)
            for row in results:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                location = MedicalRoom(row[25], row[26])
                appointments.append(Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0]))
        return appointments

    def get_appointment_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be none")
        
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        appointment = None
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id  INNER JOIN MEDICAL_ROOMS mr ON app.location = mr.room_number WHERE app.id = :id',
                id=id)
            row = results.fetchone()
            if row:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                location = MedicalRoom(row[25], row[26])
                appointment = Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0])
        return appointment

    def get_appointment_for_doctors(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        appointments = []
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id INNER JOIN MEDICAL_ROOMS mr ON app.location = mr.room_number WHERE d.id = :doctor_id',
                doctor_id=id)
            row = cursor.fetchone()
            if row:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                location = MedicalRoom(row[25], row[26])
                appointments.append(Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0]))
        return appointments

    def get_appointment_for_patients(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        appointments = []
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id INNER JOIN MEDICAL_ROOMS mr ON app.location = mr.room_number WHERE p.id = :patient_id',
                patient_id=id)
            row = cursor.fetchone()
            if row:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]))
                location = MedicalRoom(row[25], row[26])
                appointments.append(Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0]))
        return appointments

    def get_user_by_id(self, id):
        if (id is None ):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT email, password, first_name, last_name, user_type, avatar_path, id FROM medical_users WHERE id = :id",
                                     id=id)
            row = results.fetchone()
            if row:
                patient = User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6]))
        return (patient)
    
    def get_users_and_roles(self):
        users = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT email, password, first_name, last_name, 
                user_type, avatar_path, id FROM medical_users
                ORDER BY user_type, first_name ASC
                """)
            for row in results:
                users.append(User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6])))
        return (users)

    def update_appointment_status(self, id, status, room=None):
        if (id is None or status is None):
            raise ValueError("Parameters cannot be none")
        if room is not None and not isinstance(room, str):
            raise TypeError("Parameters of incorrect type")
        try:
            id = int(id)
            status = int(status)
        except:
            raise TypeError("Parameters of incorrect type")
        
        with self.__get_cursor() as cursor:
            cursor.execute("UPDATE medical_appointments SET status = :status WHERE id = :id",
                           status=status, id=id)
            if room:
                cursor.execute("UPDATE medical_appointments SET location = :room WHERE id = :id",
                           room=room, id=id)

    def get_patients_by_doctor(self, doctor_id):
        if (doctor_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            doctor_id = int(doctor_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        patients = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, users.id FROM medical_users users INNER JOIN medical_patients p ON(users.id = p.id) INNER JOIN medical_appointments appts ON(users.id = appts.patient_id) WHERE doctor_id = :id",
                id=doctor_id)
            for row in results:
                patients.append(MedicalPatient(
                    float(row[0]), row[1], row[2], row[3], row[4], str(row[5]), row[6], str(row[7]), float(row[8]), avatar_path=str(row[9]), id=int(row[10])))
        return patients

    def get_patients_by_id(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, id FROM medical_users u INNER JOIN medical_patients p USING(id) WHERE id = :id",
                                     id=patient_id)
            row = results.fetchone()
            if row:
                allergies = self.get_patient_allergies(int(row[10]))
                patient = MedicalPatient(float(row[0]), row[1], row[2], row[3], row[4], str(
                    row[5]), row[6], str(row[7]), float(row[8]), allergies=allergies, avatar_path=row[9], id=int(row[10]))
        return patient

    def get_patient_appointments(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT ma.id, ma.patient_id, ma.doctor_id, ma.appointment_time, ma.status, ma.location, ma.description, mr.room_number, mr.description FROM medical_appointments ma INNER JOIN medical_rooms mr ON mr.room_number = ma.location WHERE patient_id = :patient_id",
                patient_id=patient_id)
            for row in results:
                patient = self.get_patients_by_id(int(row[1]))
                doctor = self.get_user_by_id(int(row[2]))
                location = MedicalRoom(row[5], row[8])
                if patient is not None and doctor is not None:
                    appointments.append(Appointments(patient, doctor,
                                                     row[3], int(row[4]), location, str(row[6]), id=row[0]))
        return appointments
    
    def update_allergies(self, patient_id, allergy_ids):
        if (patient_id is None or allergy_ids is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
            for allergy in allergy_ids:
                int(allergy)
        except:
            raise TypeError("Parameters of incorrect type")
        
        with self.__get_cursor() as cursor:
            for allergy_id in allergy_ids:
                cursor.execute(
                    """
                    INSERT INTO medical_patient_allergies (patient_id, allergy_id)
                    VALUES (:patient_id, :allergy_id)
                    """,
                    patient_id=patient_id, allergy_id=allergy_id)

    def update_patient_details(self, patient_id, dob, blood_type, height, weight, allergies):
        if (patient_id is None or dob is None or blood_type is None or height is None or weight is None or allergies is None):
            raise ValueError("Parameters cannot be none")
        if (not isinstance(blood_type, str) or not isinstance(dob, date)):
            raise TypeError("Parameters of incorrect type")
            
        try:
            patient_id = int(patient_id)
            float(height)
            float(weight)
            for allergy in allergies:
                int(allergy)
        except:
            raise TypeError("Parameters of incorrect type")
        
        with self.__get_cursor() as cursor:
            cursor.execute(
                """
                MERGE INTO medical_patients p
                USING (SELECT :patient_id as id FROM dual) new_patient
                ON (p.id = new_patient.id)
                WHEN MATCHED THEN
                    UPDATE SET p.dob = :dob, p.blood_type = :blood_type, p.height = :height, p.weight = :weight
                WHEN NOT MATCHED THEN
                    INSERT (id, dob, blood_type, height, weight) VALUES (:patient_id, :dob, :blood_type, :height, :weight)
                """,
                patient_id=patient_id, dob=dob, blood_type=blood_type, height=height, weight=weight)

            cursor.execute(
                """
            DELETE FROM medical_patient_allergies
            WHERE patient_id = :patient_id
            """,
                patient_id=patient_id)

            for allergy_id in allergies:
                cursor.execute(
                    """
                    INSERT INTO medical_patient_allergies (patient_id, allergy_id)
                    VALUES (:patient_id, :allergy_id)
                    """,
                    patient_id=patient_id, allergy_id=allergy_id)

    def get_all_allergies(self):
        allergies = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, name, description FROM medical_allergies")
            for row in results:
                allergies.append({
                    'id': int(row[0]),
                    'name': str(row[1]),
                    'description': str(row[2])
                })
        return allergies

    def get_allergy_by_id(self, allergy_id):
        if (allergy_id is None):
            raise ValueError("Parameters cannot be none")
        
        try:
            allergy_id = int(allergy_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        allergy = None
        with self.__get_cursor() as cursor:
            result = cursor.execute(
                """
                SELECT id, name, description
                FROM medical_allergies
                WHERE id = :allergy_id
                """,
                allergy_id=allergy_id)
            row = result.fetchone()
            if row:
                allergy = Allergy(int(row[0]), str(row[1]), str(row[2]))
        return allergy

    def get_patient_allergies(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        allergies = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT a.id, a.name, a.description 
                FROM medical_allergies a 
                INNER JOIN medical_patient_allergies pa ON a.id = pa.allergy_id 
                WHERE pa.patient_id = :patient_id
                """,
                patient_id=patient_id)
            for row in results:
                allergies.append(
                    Allergy(int(row[0]), str(row[1]), str(row[2])))
        return allergies

    def get_patient_details(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, id FROM medical_users u INNER JOIN medical_patients p USING(id) WHERE id = :id",
                                     id=patient_id)
            row = results.fetchone()
            if row:
                patient = MedicalPatient(float(row[0]), row[1], row[2], row[3], row[4], str(
                    row[5]), row[6], str(row[7]), float(row[8]), avatar_path=row[9], id=int(row[10]))
        return patient

    def get_notes_by_patient_id(self, patient_id):
        if (patient_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            patient_id = int(patient_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        notes = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT n.id, n.note_date, n.note, p.weight, p.email, p.password, p.first_name, p.last_name, p.user_type, p.dob, p.blood_type, p.height, p.avatar_path, p.id, d.email, d.password, d.first_name, d.last_name, d.user_type, d.avatar_path, d.id, a.attachement_path FROM medical_notes n INNER JOIN medical_patients p ON (n.patient_id = p.id) INNER JOIN medical_users u ON(d.id = n.note_taker_id) INNER JOIN medical_note_attachements a ON(a.note_id = n.id) WHERE n.patient_id = :patient_id",
                patient_id=patient_id)
            for row in results:
                doctor = User(
                    row[14], row[15], row[16], row[17], row[18], avatar_path=row[19], id=int(row[20]))
                patient = MedicalPatient(float(row[3]), row[4], row[5], row[6], row[7], str(
                    row[8]), row[9], str(row[10]), float(row[11]), avatar_path=row[12], id=int(row[13]))
                attachements = self.get_attachements_by_note_id(int(row[0]))
                notes.append(Note(
                    patient, doctor, str(row[1]), str(row[2]), attachement_path=attachements, id=int(row[0])))
        return notes

    def get_note_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        note = None
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT n.id, n.note_date, n.note, p.weight, up.email, up.password, up.first_name, up.last_name, up.user_type, p.dob, p.blood_type, p.height, up.avatar_path, p.id, d.email, d.password, d.first_name, d.last_name, d.user_type, d.avatar_path, d.id, a.attachment_path
                FROM medical_notes n INNER JOIN medical_users up
                    ON (n.patient_id = up.id) INNER JOIN medical_patients p
                    ON (up.id = p.id)
                    INNER JOIN medical_users d ON(d.id = n.note_taker_id)
                    INNER JOIN medical_note_attachments a ON(a.note_id = n.id)
                WHERE n.id = :id
                """,
                id=id)
            row = results.fetchone()
            if row:
                doctor = User(
                    row[14], row[15], row[16], row[17], row[18], avatar_path=row[19], id=int(row[20]))
                patient = MedicalPatient(float(row[3]), row[4], row[5], row[6], row[7], str(
                    row[8]), row[9], str(row[10]), float(row[11]), avatar_path=row[12], id=int(row[13]))
                attachements = self.get_attachements_by_note_id(int(row[0]))
                note = (Note(
                    patient, doctor, row[1], str(row[2]), attachement_path=attachements, id=int(row[0])))
        return note

    def get_notes_by_doctor_id(self, doctor_id):
        if (doctor_id is None):
            raise ValueError("Parameters cannot be none")
        try:
            doctor_id = int(doctor_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        
        notes = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT n.id, n.note_date, n.note, p.weight, up.email, up.password, up.first_name, up.last_name, up.user_type, p.dob, p.blood_type, p.height, up.avatar_path, p.id, d.email, d.password, d.first_name, d.last_name, d.user_type, d.avatar_path, d.id, a.attachment_path
                FROM medical_notes n INNER JOIN medical_users up
                    ON (n.patient_id = up.id) INNER JOIN medical_patients p
                    ON (up.id = p.id)
                    INNER JOIN medical_users d ON(d.id = n.note_taker_id)
                    INNER JOIN medical_note_attachments a ON(a.note_id = n.id)
                WHERE note_taker_id = :doctor_id
                """,
                doctor_id=doctor_id)
            for row in results:
                doctor = User(
                    row[14], row[15], row[16], row[17], row[18], avatar_path=row[19], id=int(row[20]))
                patient = MedicalPatient(float(row[3]), row[4], row[5], row[6], row[7], str(
                    row[8]), row[9], str(row[10]), float(row[11]), avatar_path=row[12], id=int(row[13]))
                attachements = self.get_attachements_by_note_id(int(row[0]))
                notes.append(Note(
                    patient, doctor, row[1], str(row[2]), attachements, id=int(row[0])))
        return notes

    def get_attachements_by_note_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        attachements = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                """
                SELECT a.attachment_path
                FROM medical_notes n INNER JOIN medical_note_attachments a 
                ON(a.note_id = n.id)
                WHERE n.id = :note_id
                """,
                note_id=id)
            for row in results:
                attachements.append(str(row[0]))
        return attachements

    def create_note(self, note):
        if not isinstance(note, Note):
            raise TypeError("expected Note object")
        with self.__get_cursor() as cursor:
            new_id = cursor.var(oracledb.NUMBER)
            cursor.execute('insert into medical_notes (patient_id, note_taker_id, note_date, note)  values (:patient_id, :note_taker_id, :note_date, :note) returning id into :id',
                           patient_id=note.patient.id,
                           note_taker_id=note.note_taker.id,
                           note_date=note.note_date,
                           note=note.note,
                           id=new_id)
            note_id = int(new_id.values[0][0])
            for path in note.attachement_path:
                cursor.execute('insert into medical_note_attachments (note_id, attachment_path)  values (:note_id, :attachement_path)',
                               note_id=note_id,
                               attachement_path=str(path))
                

    def update_note(self, note, paths):
        if not isinstance(note, Note):
            raise TypeError("expected Note object")
        with self.__get_cursor() as cursor:
            for path in paths:
                cursor.execute('insert into medical_note_attachments (note_id, attachment_path)  values (:note_id, :attachement_path)',
                               note_id=note.id,
                               attachement_path=str(path))

    def create_user(self, user):
        if not isinstance(user, User):
            raise TypeError("expected User object")
        with self.__get_cursor() as cursor:
            cursor.execute('insert into medical_users (email, password, first_name,last_name,user_type)  values (:email, :password, :first_name, :last_name, :user_type)',
                           email=user.email,
                           password=user.password,
                           first_name=user.first_name,
                           last_name=user.last_name,
                           user_type=user.access_level)

    def update_user_password(self, user_id, new_password_hash):
        if (user_id is None or new_password_hash is None):
            raise ValueError("Parameters cannot be empty")
        try:
            user_id = int(user_id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        with self.__get_cursor() as cursor:
            cursor.execute(
                "UPDATE medical_users SET password = :password WHERE id = :id",
                password=new_password_hash, id=user_id
            )

    def get_user_by_email(self, email):
        if (not isinstance(email, str)):
            raise ValueError("Parameters cannot be none")
        
        user = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'select email, password, first_name, last_name, user_type, avatar_path, id from medical_users where email=:email', email=email)
            row = cursor.fetchone()
            if row:
                user = User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6]))
        return user

    def update_user_avatar(self, id, avatar_path):
        if (id is None or (avatar_path is not None and not isinstance(avatar_path, str))):
            raise ValueError("Parameters cannot be none")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        with self.__get_cursor() as cursor:
            cursor.execute(
                'SELECT AVATAR_PATH FROM medical_users WHERE id = :id',
                id=id)
            result = cursor.fetchone()
            if result is None:
                cursor.execute(
                    'INSERT INTO medical_users (id, AVATAR_PATH) VALUES (:id, :avatar_path)',
                    id=id, avatar_path=avatar_path)
            else:
                cursor.execute(
                    'UPDATE medical_users SET AVATAR_PATH = :avatar_path WHERE id = :id',
                    id=id, avatar_path=avatar_path)

    def add_appointment(self, appointment):
        with self.__get_cursor() as cursor:
            if not isinstance(appointment, Appointments):
                raise TypeError("expected Appointment object")
            with self.__get_cursor() as cursor:
                id = cursor.var(oracledb.NUMBER)
                cursor.execute('insert into medical_appointments (patient_id, doctor_id, appointment_time, status, location, description) values (:patient_id, :doctor_id, :appointment_time, :status, :location, :description) returning id into :id',
                               patient_id=appointment.patient.id,
                               doctor_id=appointment.doctor.id,
                               appointment_time=appointment.appointment_time,
                               status=appointment.status,
                               location=appointment.location.room_number,
                               description=appointment.description,
                               id=id)
                new_id = id.values[0][0]
                return new_id

    def delete_appointment_by_id(self, id):
        if (id is None):
            raise ValueError("Parameters cannot be None")
        try:
            id = int(id)
        except:
            raise TypeError("Parameters of incorrect type")
        
        with self.__get_cursor() as cursor:
            with self.__get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM medical_appointments WHERE id = :id", id=id)
                cursor.execute(
                    "DELETE FROM medical_appointments WHERE id = :id", id=id)

    def update_appointment(self, appointment):
        with self.__get_cursor() as cursor:
            if not isinstance(appointment, Appointments):
                raise TypeError("expected type of Appointmentsr")
            with self.__get_cursor() as cursor:
                cursor.execute(" UPDATE medical_appointments SET patient_id =: patient_id, doctor_id =: doctor_id, appointment_time =: appointment_time, status =: status, location =: location, description =: description WHERE id =:id",
                               patient_id=appointment.patient.id, doctor_id=appointment.doctor.id, appointment_time=appointment.appointment_time, status=appointment.status, location=appointment.location, description=appointment.description, id=appointment.id)
                cursor.execute(" UPDATE medical_appointments SET patient_id =: patient_id, doctor_id =: doctor_id, appointment_time =: appointment_time, status =: status, location =: location, description =: description WHERE id =:id",
                               patient_id=appointment.patient.id, doctor_id=appointment.doctor.id, appointment_time=appointment.appointment_time, status=appointment.status, location=appointment.location, description=appointment.description, id=appointment.id)

    def get_appointments(self):
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute('SELECT app.id, app.patient_id, app.doctor_id, app.appointment_time, app.status, app.location, app.description, d.ID, d.EMAIL, d.PASSWORD, d.FIRST_NAME, d.LAST_NAME, d.USER_TYPE, d.AVATAR_PATH, p.id, p.EMAIL, p.PASSWORD, p.FIRST_NAME, p.LAST_NAME, p.USER_TYPE, p.AVATAR_PATH, mp.DOB, mp.BLOOD_TYPE, mp.HEIGHT, mp.WEIGHT, mr.room_number, mr.description FROM medical_appointments app INNER JOIN medical_users d ON app.doctor_id = d.id INNER JOIN medical_users p ON app.PATIENT_ID = p.ID INNER JOIN MEDICAL_PATIENTS mp ON mp.id = p.id INNER JOIN MEDICAL_ROOMs mr ON app.location = mr.room_number')
            for row in results:
                doctor = User(row[8], row[9], row[10], row[11],
                              row[12], avatar_path=row[13], id=int(row[7]))
                allergies = self.get_patient_allergies(int(row[14]))
                patient = MedicalPatient(float(row[24]), row[15], row[16], row[17], row[18], row[19], row[21], row[22], float(
                    row[23]), avatar_path=row[20], id=int(row[14]), allergies=allergies)
                location = MedicalRoom(row[25], row[26])
                appointments.append(Appointments(
                    patient, doctor, row[3], row[4], location, str(row[6]), id=row[0]))
        return appointments

    def get_medical_rooms(self):
        medical_rooms = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'SELECT room_number, description FROM medical_rooms')
            for row in results:
                medical_room = MedicalRoom(row[0], str(row[1]))
                medical_rooms.append(medical_room)
        return medical_rooms

    def get_medical_room_by_room_number(self,room_number):
        if (not isinstance(room_number, str)):
            raise ValueError("Parameters cannot be none")
        
        medical_room = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'select room_number, description FROM medical_rooms where room_number=:room_number', room_number=room_number)
            row = cursor.fetchone()
            if row:
                medical_room = MedicalRoom(row[0], row[1])
        return medical_room

    def __get_cursor(self):
        for i in range(3):
            try:
                return self.__connection.cursor()
            except Exception as e:
                # Might need to reconnect
                self.__reconnect()

    def __reconnect(self):
        try:
            self.close()
        except oracledb.Error as f:
            pass
        self.__connection = self.__connect()

    def __connect(self):
        return oracledb.connect(user=os.environ['DBUSER'], password=os.environ['DBPWD'],
                                host="198.168.52.211", port=1521, service_name="pdbora19c.dawsoncollege.qc.ca")

    def close(self):
        '''Closes the connection'''
        if self.__connection is not None:
            self.__connection.close()
            self.__connection = None


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')
