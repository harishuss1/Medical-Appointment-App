from datetime import date
import datetime
import json
import unittest

from flask import jsonify
from flask_login import current_user, login_user
from MedicalApp import create_app
from MedicalApp.db.dbmanager import get_db
from MedicalApp.user import MedicalPatient


class PatientAPITestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_getpatients_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(2, len(results))
        self.assertEqual("Maddie", results[0]['first_name'])
        self.assertEqual("Buckley", results[0]['last_name'])
        self.assertEqual("maddie@example.com", results[0]['email'])
        self.assertEqual(1, len(results[0]['allergies']))
        self.assertEqual('1', results[0]['allergies'][0].split("/")[-1])
        self.assertEqual('68.0', results[0]['weight'])
    
    #page correctly defaults to 1!
    def test_getpatients_goodfirstname_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?first=Maddie', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Maddie", results[0]['first_name'])
        self.assertEqual("Buckley", results[0]['last_name'])
        self.assertEqual("maddie@example.com", results[0]['email'])
        self.assertEqual(1, len(results[0]['allergies']))
        self.assertEqual('1', results[0]['allergies'][0].split("/")[-1])
        self.assertEqual('68.0', results[0]['weight'])
        
    def test_getpatients_firstnamenotexist_404(self): #SHOULD THIS REALLY THROW 404???
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?first=Buck', headers=headers)
        self.assertEqual(404, result.status_code)
        
    def test_getpatients_goodlastname_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?last=Buckley', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Maddie", results[0]['first_name'])
        self.assertEqual("Buckley", results[0]['last_name'])
        self.assertEqual("maddie@example.com", results[0]['email'])
        self.assertEqual(1, len(results[0]['allergies']))
        self.assertEqual('1', results[0]['allergies'][0].split("/")[-1])
        self.assertEqual('68.0', results[0]['weight'])
        
    def test_getpatients_lastnamenotexist_404(self): #SHOULD THIS REALLY THROW 404???
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?last=Buck', headers=headers)
        self.assertEqual(404, result.status_code)
        
    def test_getpatients_page_success(self): #SHOULD THIS REALLY THROW 404???
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?page=2', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Eddie", results[0]['first_name'])
        self.assertEqual("Diaz", results[0]['last_name'])
        self.assertEqual("eddie@example.com", results[0]['email'])
        self.assertEqual(0, len(results[0]['allergies']))
        self.assertEqual('75.2', results[0]['weight'])
        
    def test_getpatients_incorrectpagetype_400(self): #SHOULD THIS REALLY THROW 404???
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients?page=jjjj', headers=headers)
        self.assertEqual(400, result.status_code)
        
    def test_getpatients_notoken_401(self):
        result = self.client.get('/api/patients/6')
        self.assertEqual(401, result.status_code)
        
    def test_getpatients_insufficientpermission_401(self):
        token = "2z12xfm3gqvZr1kZIAi4YXahpeA"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients', headers=headers)
        self.assertEqual(401, result.status_code)
        
    def test_getpatient_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients/6', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json
        self.assertIsNotNone(results)
        self.assertEqual("Maddie", results['first_name'])
        self.assertEqual("Buckley", results['last_name'])
        self.assertEqual("maddie@example.com", results['email'])
        self.assertEqual(1, len(results['allergies']))
        self.assertEqual('1', results['allergies'][0].split("/")[-1])
        self.assertEqual('68.0', results['weight'])
        
    def test_getpatient_notoken_401(self):
        result = self.client.get('/api/patients/6')
        self.assertEqual(401, result.status_code)
        
    def test_getpatient_insufficientpermission_401(self):
        token = "2z12xfm3gqvZr1kZIAi4YXahpeA"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients/6', headers=headers)
        self.assertEqual(401, result.status_code)
        
    def test_getpatient_doesnotexist_404(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients/100', headers=headers)
        self.assertEqual(404, result.status_code)
        
    def test_getpatient_doesnotexist_404(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/patients/100', headers=headers)
        self.assertEqual(404, result.status_code)
        
    def test_addallergy_success_201(self):
        data = {
        }
        data['allergies'] = [1]
        json_string = json.dumps(data)
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put('/api/patients/7', headers=headers, data=json_string, content_type='application/json')
        self.assertEqual(201, result.status_code)
        # print(result)
        self.assertNotEqual("", result.headers['Patient'])


if __name__ == '__main__':
    unittest.main()