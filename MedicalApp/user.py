import datetime
import json
from flask_login import UserMixin
from MedicalApp.allergy import Allergy


class User(UserMixin):
    def __init__(self, email, password, first_name, last_name, access_level="PATIENT", avatar_path=None, id=None):
        if not isinstance(email, str):
            raise ValueError("Illegal type for email")
        if not isinstance(password, str):
            raise ValueError("Illegal type for password")
        if not isinstance(first_name, str):
            raise ValueError("Illegal type for first name")
        if not isinstance(last_name, str):
            raise ValueError("Illegal type for last name")
        if not isinstance(access_level, str):
            raise ValueError("Illegal type for access level")
        if avatar_path != None and not isinstance(avatar_path, str):
            raise ValueError("Illegal type for avatar path")
        if id != None and not isinstance(id, int):
            raise ValueError("Illegal type for avatar path")

        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.access_level = access_level
        self.avatar_path = avatar_path

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class MedicalPatient(User):
    def __init__(self, weight, email, password, first_name, last_name, access_level, dob, blood_type, height, allergies=None, avatar_path=None, id=None):
        super().__init__(email, password, first_name,
                         last_name, access_level, avatar_path, id)
        if not isinstance(dob, datetime.date):
            raise ValueError("Illegal type for dob")
        if not isinstance(blood_type, str):
            raise ValueError("Illegal type for blood type")
        if not isinstance(height, float):
            raise ValueError("Illegal type for height")
        if not isinstance(weight, float):
            raise ValueError("Illegal type for weight")
        if allergies is not None and not all(isinstance(alleg, Allergy) for alleg in allergies):
            raise ValueError("All allergies must be strings")
        self.dob = dob
        self.blood_type = blood_type
        self.height = height
        self.weight = weight
        self.allergies = allergies if allergies is not None else []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def to_json(self):
        data = {}
        data['id'] = str(self.id)
        data['avatar_path'] = str(self.avatar_path)
        #data['allergies'] = url_for(allergy)
        data['email'] = str(self.email)
        data['password'] = str(self.password)
        data['first_name'] = str(self.first_name)
        data['last_name'] = str(self.last_name)
        data['access_level'] = str(self.access_level)
        data['dob'] = str(self.dob)
        data['blood_type'] = str(self.blood_type)
        data['height'] = str(self.height)
        data['weight'] = str(self.weight)
        return data