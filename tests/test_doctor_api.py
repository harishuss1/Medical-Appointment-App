import unittest
import json
from MedicalApp import create_app

class TestDoctorAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_get_doctors(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/doctors/', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(8, len(results))
        self.assertEqual("Eddie", results[2]['first_name'])
        self.assertEqual("Diaz", results[2]['last_name'])
        self.assertEqual("eddie@example.com", results[2]['email'])

    def test_get_doctor(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/doctors/1', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json
        self.assertIsNotNone(results)
        self.assertEqual("Eddie", results[0]['first_name'])
        self.assertEqual("Diaz", results[0]['last_name'])
        self.assertEqual("eddie@example.com", results[0]['email'])

    def test_get_doctor_error(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/doctors/9999', headers=headers)
        self.assertEqual(404, result.status_code)

        result = self.client.get('/api/doctors/test', headers=headers)
        self.assertEqual(404, result.status_code)

    def test_get_doctor_notoken_401(self):
        result = self.client.get('/api/doctors/1')
        self.assertEqual(401, result.status_code)



if __name__ == '__main__':
    unittest.main()