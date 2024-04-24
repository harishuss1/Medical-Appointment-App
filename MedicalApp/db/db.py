import oracledb
import os
from flask import g
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
        try:
            with self.__connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE medical_users SET account_status = 'blocked' WHERE email = :email",
                    {'email': email}
                )
                self.__connection.commit()
        except Exception as e:
            print("Error blocking user:", e)
            raise
        
    def change_user_type(self, user_email, new_user_type):
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
                'select id, email, password, first_name, last_name,avatar_path,user_type from medical_users where email=:email', email=email)
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], row[2],
                            row[3], row[4], row[5], row[6])
        return user
    
    def add_appointment(self, appointment):
        with self.__get_cursor() as cursor:
            if not isinstance(appointment, Appointments):
                raise TypeError("expected Appointment object")
            with self.__get_cursor() as cursor:
                cursor.execute('insert into medical_appointments (id, patient_id, doctor_id, appointment_time, status, location, description) values (:id, :patient_id, :doctor_id, :appointment_time, :status, :location, :description)',
                            id=appointment.id,
                            patient_id=appointment.patient_id,
                            doctor_id=appointment.doctor_id,
                            appointment_time=appointment.appointment_time,
                            status=appointment.status,
                            location=appointment.location,
                            description=appointment.description)

    def get_appointment_id(self, id):
        appointment = None
        with self.__get_cursor() as cursor:
            cursor.execute(
                'select id, patient_id, doctor_id, appointment_time, status, location, description from medical_appointments where name=:name', id=id)
            row = cursor.fetchone()
            if row:
                appointment = Appointments(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6])
        return appointment

    def get_appointments(self):
        appointments = []
        with self.__get_cursor() as cursor:
            results = cursor.execute(
                'select id, patient_id, doctor_id, appointment_time, status, location, description from medical_appointments')
            for row in results:
                appointment = Appointments(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                appointments.append(appointment)
        return appointments


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


if __name__ == '__main__':
    print('Provide file to initialize database')
    file_path = input()
    if os.path.exists(file_path):
        db = Database()
        db.run_file(file_path)
        db.close()
    else:
        print('Invalid Path')

