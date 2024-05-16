from datetime import date
import datetime
import json
import unittest

from flask import jsonify
from flask_login import current_user, login_user
from MedicalApp import create_app
from MedicalApp.user import MedicalPatient


class AllergyAPITestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_getallergies_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(2, len(results))
        self.assertEqual("Peanuts", results[0]['name'])
        self.assertEqual("Allergic reaction to peanuts causing hives and swelling.", results[0]['description'])
        self.assertEqual(1, results[0]['id'])

    #page correctly defaults to 1!
    def test_getallergies_goodname_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies?name=Peanuts', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Peanuts", results[0]['name'])
        self.assertEqual("Allergic reaction to peanuts causing hives and swelling.", results[0]['description'])
        self.assertEqual(1, results[0]['id'])
        
    def test_getallergies_namenotexist_404(self): #SHOULD THIS REALLY THROW 404???
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies?name=Buck', headers=headers)
        self.assertEqual(404, result.status_code)

        
    def test_getallergies_page_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies?page=2', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Blueberries", results[0]['name'])
        self.assertEqual("Allergic reaction to blueberries causing hives and swelling.", results[0]['description'])
        self.assertEqual(3, results[0]['id'])
        
    def test_getallergies_incorrectpagetype_400(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies?page=jjjj', headers=headers)
        self.assertEqual(400, result.status_code)
        
    def test_getallergies_notoken_401(self):
        result = self.client.get('/api/allergies/6')
        self.assertEqual(401, result.status_code)
        
    # def test_getallergies_insufficientpermission_403(self): SIMULATING LOGIN???
    #     token = "2z12xfm3gqvZr1kZIAi4YXahpeA"
    #     headers = {'Authorization': f'Bearer {token}'}
    #     result = self.client.get('/api/allergies', headers=headers)
    #     self.assertEqual(403, result.status_code)
        
    def test_getallergy_success(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies/1', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json
        self.assertIsNotNone(results)
        self.assertEqual("Peanuts", results['name'])
        self.assertEqual("Allergic reaction to peanuts causing hives and swelling.", results['description'])
        self.assertEqual(1, results['id'])
        
    def test_getallergy_notoken_401(self):
        result = self.client.get('/api/allergies/2')
        self.assertEqual(401, result.status_code)
        
    # def test_getpatient_insufficientpermission_401(self):
    #     token = "2z12xfm3gqvZr1kZIAi4YXahpeA"
    #     headers = {'Authorization': f'Bearer {token}'}
    #     result = self.client.get('/api/patients/6', headers=headers)
    #     self.assertEqual(401, result.status_code)
        
    def test_getallergy_doesnotexist_404(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/allergies/100', headers=headers)
        self.assertEqual(404, result.status_code)

if __name__ == '__main__':
    unittest.main()