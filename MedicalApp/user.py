from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email, password, first_name, last_name, access_level="patient", avatar_path=None, id=None):
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
        


class MedicalPatient(User):
    def __init__(self, weight, email, password, first_name, last_name, access_level, dob, blood_type, height, avatar_path=None, id=None):
        super().__init__(email, password, first_name,
                         last_name, access_level, avatar_path, id)
        if not isinstance(dob, str):
            raise ValueError("Illegal type for dob")
        if not isinstance(blood_type, str):
            raise ValueError("Illegal type for blood type")
        if not isinstance(height, float):
            raise ValueError("Illegal type for height")
        if not isinstance(weight, float):
            raise ValueError("Illegal type for weight")
        self.dob = dob
        self.blood_type = blood_type
        self.height = height
        self.weight = weight
