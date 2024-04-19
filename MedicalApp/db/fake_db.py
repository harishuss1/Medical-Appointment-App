from .user import User, MedicalPatient
from oracledb import IntegrityError


class FakeDB:

    def __init__(self):
        self.users = []

    def run_file(self, file_path):
        pass

    def close(self):
        pass
