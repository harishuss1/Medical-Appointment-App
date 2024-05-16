from datetime import date
import datetime
import unittest
from MedicalApp import create_app
from MedicalApp.user import MedicalPatient


class MedicalPatientTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_createpatient_successful(self):
        med_patient = MedicalPatient(150.0, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180.0, avatar_path="/instance/1/bob.png")
        self.assertEqual(150, med_patient.weight)
        self.assertEqual("patient@patient.com", med_patient.email)
        self.assertEqual("1234567", med_patient.password)
        self.assertEqual("Bob", med_patient.first_name)
        self.assertEqual("Nash", med_patient.last_name)
        self.assertEqual('PATIENT', med_patient.access_level)
        self.assertEqual(datetime.date(1968, 5, 17), med_patient.dob)
        self.assertEqual("A+", med_patient.blood_type)
        self.assertEqual(180, med_patient.height)
        self.assertEqual("/instance/1/bob.png", med_patient.avatar_path)
        self.assertEqual([], med_patient.allergies)
        self.assertIsNone(med_patient.id)
        
    def test_createpatient_badweight(self):
        def create_patient():
            med_patient = MedicalPatient("150", "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_noneweight(self):
        def create_patient():
            med_patient = MedicalPatient(None, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_bademail(self):
        def create_patient():
            med_patient = MedicalPatient(150, 333, "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_noneemail(self):
        def create_patient():
            med_patient = MedicalPatient(150, None, "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badpassword(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", 3333, "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonepassword(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", None, "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badfirstname(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", 1483, "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonefirstname(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", None, "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badlastname(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", 18932, "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonelastname(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", None, "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badaccesslevel(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", 12345, datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_noneaccesslevel(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", None, datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_baddate(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", "date.datetime(1968, 5, 17)", "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonedate(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", None, "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
    
    def test_createpatient_badbloodtype(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), 1820, 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonebloodtype(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), None, 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badpath(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path=12345)
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_nonepath(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path=None)
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_badheight(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", 180, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
    def test_createpatient_noneheight(self):
        def create_patient():
            med_patient = MedicalPatient(150, "patient@patient.com", "1234567", "Bob", "Nash", "PATIENT", datetime.date(1968, 5, 17), "A+", None, avatar_path="/instance/1/bob.png")
        self.assertRaises(ValueError, create_patient)
        
if __name__ == '__main__':
    unittest.main()