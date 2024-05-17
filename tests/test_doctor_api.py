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
        result = self.client.get(
            '/api/doctors', headers=headers, follow_redirects=True)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(1, len(results))
        self.assertEqual("Bobby", results[0]['first_name'])
        self.assertEqual("Nash", results[0]['last_name'])
        self.assertEqual("bobby@example.com", results[0]['email'])

    def test_get_doctor(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/doctors/9', headers=headers)
        self.assertEqual(200, result.status_code)
        doctor = result.json
        self.assertIsNotNone(doctor)
        self.assertEqual("Bobby", doctor['first_name'])
        self.assertEqual("Nash", doctor['last_name'])
        self.assertEqual("bobby@example.com", doctor['email'])

    def test_get_doctor_error(self):
        token = "km9b5-UeGr3SDy6PszxFZRRvqiE"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/doctors/9999', headers=headers)
        self.assertEqual(404, result.status_code)

        result = self.client.get('/api/doctors/test', headers=headers)
        self.assertEqual(404, result.status_code)


if __name__ == '__main__':
    unittest.main()
