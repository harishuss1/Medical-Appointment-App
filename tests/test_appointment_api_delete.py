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
        # Assume appointment_id is 1
        appointment_id = 1
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        create_result = self.client.delete(f'/api/appointments/{appointment_id}', headers=headers, content_type='application/json',follow_redirects=True)

        # Check if the appointment was deleted successfully
        self.assertEqual(204, create_result.status_code)

    def test_delete_nonexistent_appointment_abort_401(self):
        # appointment id = 999  which does not exist
        appointment_id = 999
        token = "dontexist"
        headers = {'Authorization': f'Bearer {token}'}
        
        #delete appointment
        delete_result = self.client.delete(f'/api/appointments/{appointment_id}', headers=headers)
        
        self.assertEqual(401, delete_result.status_code)

    def test_delete_noaccess_abort_403(self):
        appointment_id = 1
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        
        #delete appointment
        delete_result = self.client.delete(f'/api/appointments/{appointment_id}', headers=headers)
        
        self.assertEqual(403, delete_result.status_code)


if __name__ == '__main__':
    unittest.main()
