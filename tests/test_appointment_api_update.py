import json
import unittest
import datetime
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
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
        
    # def test_update_appointment_invalid_data(self):
        
    #     updated_appointment_data = {
    #         "doctor_id": "invalid_id",  
    #         "appointment_time": "2025-01-01", 
    #         "description": "" 
    #     }
        
    #     json_data = json.dumps(updated_appointment_data)
        
    #     token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
    #     headers = {'Authorization': f'Bearer {token}'}
    #     update_response = self.client.put(f'/api/appointments/1', data=json_data, headers=headers, content_type='application/json')
        
    #     self.assertEqual(400, update_response.status_code)
        
if __name__ == '__main__':
    unittest.main()