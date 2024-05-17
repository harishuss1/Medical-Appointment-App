import json
import unittest
import datetime
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
from MedicalApp.db.dbmanager import get_db
from MedicalApp.user import User, MedicalPatient
from MedicalApp.medical_room import MedicalRoom

class AppointmentsUpdateTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app(test_config={})
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_addappt_success_201(self):
        data = {
        }
        data['doctor_id'] = 9
        data['appointment_time'] = "2025-01-01"
        data['description'] = "checkuppppp"
        json_string = json.dumps(data)
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put('/api/appointments/1', data=json_string, headers=headers, content_type='application/json')
        self.assertEqual(201, result.status_code)
        self.assertNotEqual("", result.headers['Appointment'])
        self.assertNotEqual(9, result.headers['Appointment'].split("/")[-1])
        
    def test_update_appointment_patient_invalid_id(self):
        
        updated_appointment_data = {
            "doctor_id": "invalid_id",  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy" 
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(400, result.status_code)
        
    def test_update_appointment_patient_invalid_doctor(self):
        
        updated_appointment_data = {
            "doctor_id": 1,
            "appointment_time": "2025-01-01", 
            "description": "yayyyy" 
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        response_data = json.loads(result.get_data(as_text=True))
        self.assertEqual(404, result.status_code)
        
    def test_update_appointment_patient_invalid_id(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025/01/01", 
            "description": "yayyyy" 
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(400, result.status_code)
        
    def test_update_appointment_patient_invalid_date(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025/01/01", 
            "description": "yayyyy" 
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(400, result.status_code)
        
    def test_update_appointment_patient_ignores_excess_data(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy",
            "status": -1,
            "location": "105"
            
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(201, result.status_code)
        self.assertEqual('1', result.headers['Appointment'].split("/")[-1])
        appointment = get_db().get_appointment_by_id(1)
        self.assertEqual("yayyyy", appointment.description)
        self.assertEqual(0, appointment.status)
        
    def test_update_appointment_patient_nofields_400(self):
        
        updated_appointment_data = {
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(400, result.status_code)
        
    def test_update_appointment_doctor_ignoreexcessfields_201(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy",
            "status": 1,
            "location": "105"
            
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
        self.assertEqual(201, result.status_code)
        self.assertEqual('1', result.headers['Appointment'].split("/")[-1])
        appointment = get_db().get_appointment_by_id(1)
        self.assertEqual("Regular checkup", appointment.description)
        self.assertEqual("105", appointment.location.room_number)
        self.assertEqual(1, appointment.status)
        
    def test_update_appointment_doctor_roomnotexist_404(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy",
            "status": 1,
            "location": "106"
            
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        # response_data = json.loads(result.get_data(as_text=True))
        # print(response_data['description'])
        self.assertEqual(404, result.status_code)
        
    def test_update_appointment_doctor_badstatus_404(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy",
            "status": -2,
            "location": "105"
            
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        # response_data = json.loads(result.get_data(as_text=True))
        # print(response_data['description'])
        self.assertEqual(404, result.status_code)
        
    def test_update_appointment_doctor_badstatustype_400(self):
        
        updated_appointment_data = {
            "doctor_id": 9,  
            "appointment_time": "2025-01-01", 
            "description": "yayyyy",
            "status": "blahh",
            "location": "105"
            
        }
        
        json_data = json.dumps(updated_appointment_data)
        
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        # response_data = json.loads(result.get_data(as_text=True))
        # print(response_data['description'])
        self.assertEqual(400, result.status_code)
        
if __name__ == '__main__':
    unittest.main()