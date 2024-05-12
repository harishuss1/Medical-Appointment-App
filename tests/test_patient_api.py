from datetime import date
import datetime
import unittest
from MedicalApp import create_app
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
        result = self.client.get('/api/patients')
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

if __name__ == '__main__':
    unittest.main()