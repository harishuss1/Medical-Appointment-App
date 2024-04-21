import oracledb
import os
from flask import g
from werkzeug.security import generate_password_hash


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
    
    def create_user(self, email, plaintext_password, first_name, last_name, user_type):
        # Hash the password securely
        hashed_password = generate_password_hash(plaintext_password, method='pbkdf2:sha256', salt_length=16)

        with self.__connection.cursor() as cursor:
            insert_query = """
                INSERT INTO medical_users (email, password, first_name, last_name, user_type)
                VALUES (:email, :password, :first_name, :last_name, :user_type)
            """
            cursor.execute(insert_query, {
                'email': email,
                'password': hashed_password,
                'first_name': first_name,
                'last_name': last_name,
                'user_type': user_type
            })
    
