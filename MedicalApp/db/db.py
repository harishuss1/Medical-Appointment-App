import oracledb
import os
from flask import g
from ..appointments import Appointments
from ..user import MedicalPatient
from ..note import Note
from MedicalApp.user import User


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

    # status 0 = pending, status 1 = confirmed, status -1 = cancel
    def get_appointments_by_status(self, status):
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, patient_id, doctor_id, appointment_time, status, location, description FROM medical_appointments WHERE status = :status",
                status=status)
            for row in results:
                appointments.append(Appointments(int(row[0]), int(row[1]), int(
                    row[2]), str(row[3]), int(row[4]), row[5], str(row[6])))
        return appointments

    def get_appointment_by_id(self, id):
        appointment = None
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, patient_id, doctor_id, appointment_time, status, location, description FROM medical_appointments WHERE id = :id",
                id=id)
            row = results.fetchone()
            if row:
                appointment = Appointments(int(row[0]), int(row[1]), int(
                    row[2]), str(row[3]), int(row[4]), row[5], row[6])
        return appointment

    def get_user_by_id(self, id):
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT email, password, first_name, last_name, user_type, avatar_path, id FROM medical_users WHERE id = :id",
                                     id=id)
            row = results.fetchone()
            if row:
                patient = User(
                    row[0], row[1], row[2], row[3], row[4], avatar_path=row[5], id=int(row[6]))
        return (patient)

    def update_appointment_status(self, id, status):
        with self.__get_cursor() as cursor:
            cursor.execute("UPDATE medical_appointments SET status = :status WHERE id = :id",
                           status=status, id=id)
            
    def get_patients_by_doctor(self, doctor_id):
        patients = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, users.id FROM medical_users users INNER JOIN medical_patients p ON(users.id = p.id) INNER JOIN medical_appointments appts ON(users.id = appts.patient_id) WHERE doctor_id = :id",
                id=doctor_id)
            for row in results:
                patients.append(MedicalPatient(
                    float(row[0]), row[1], row[2], row[3], row[4], str(row[7]), str(row[8]), float(row[9]), avatar_path=row[5], id=int(row[6]) ))
        return patients
    
    def get_patients_by_id(self, patient_id):
        patient = None
        with self.__get_cursor() as cursor:
            results = cursor.execute("SELECT weight, email, password, first_name, last_name, user_type, dob, blood_type, height, avatar_path, id FROM medical_users u INNER JOIN medical_patients p USING(id) WHERE id = :id",
                                     id=patient_id)
            row = results.fetchone()
            if row:
                patient = MedicalPatient(
                    float(row[0]), row[1], row[2], row[3], row[4], str(row[7]), str(row[8]), float(row[9]), avatar_path=row[5], id=int(row[6]) )
        return (patient)
    
    def get_notes_by_patient_id(self, patient_id, doctor_id):
        notes = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                "SELECT id, patient_id, note_taker_id, note_date, note FROM medical_notes WHERE note_taker_id = :doctor_id AND patient_id = :patient_id",
                doctor_id=doctor_id, patient_id=patient_id)
            for row in results:
                notes.append(Note(
                    int(row[0]), int(row[1]), int(row[2]), str(row[3]), str(row[4])))
        return notes

    def create_user(self, user):
        if not isinstance(user, User):
            raise TypeError("expected User object")
        with self.__get_cursor() as cursor:
            cursor.execute('insert into medical_users (email, password, first_name,last_name,avatar_path,user_type)  values (:email, :password, :first_name, :last_name, :access_level)', {
                           'email': user.email,
                           'password': user.password,
                           'first_name': user.first_name,
                           'last_name': user.last_name,
                           'user_type': user.access_level})

    def get_user_by_email(self, email):
        user = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'select id, email, password, first_name, last_name,avatar_path,user_typefrom medical_users where email=:email', email=email)
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], row[2],
                            row[3], row[4], row[5], row[6])
        return user

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
