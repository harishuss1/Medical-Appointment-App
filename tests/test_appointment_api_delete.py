from datetime import datetime
import json
import unittest
from flask import jsonify
from flask_login import current_user, login_user
from oracledb import DatabaseError
from MedicalApp import create_app
from MedicalApp.appointments import Appointments
from unittest.mock import patch


class AppointmentAPITestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_delete_appointment_success_204(self):
        # Assume appointment_id is 1 for this example
        appointment_id = 1
        token = "your_token_here"
        headers = {'Authorization': f'Bearer {token}'}

        #create an appointment 
        data = {
            "doctor_id": 9,
            "appointment_time": "2025-01-01",
            "description": "checkuppppp"
        }
        json_string = json.dumps(data)
        create_result = self.client.post('/api/appointments', data=json_string, headers=headers, content_type='application/json',follow_redirects=True)

        # Check the appointment was created 
        self.assertEqual(201, create_result.status_code)
        # Get the URL of new created appointment
        appointment_url = create_result.headers['URL']  

        #delete the appointment
        delete_result = self.client.delete(appointment_url, headers=headers)

        # Check if the appointment was deleted successfully
        self.assertEqual(204, delete_result.status_code)

    def test_delete_nonexistent_appointment(self):
        # appointment id = 999  which does not exist
        appointment_id = 999
        token = "dontexist"
        headers = {'Authorization': f'Bearer {token}'}
        
        #delete appointment
        delete_result = self.client.delete(f'/api/appointments/{appointment_id}', headers=headers)
        
        self.assertEqual(401, delete_result.status_code)


if __name__ == '__main__':
    unittest.main()
