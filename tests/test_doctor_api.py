import unittest
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
        result = self.client.get('/api/doctors/')
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertTrue('count' in result.json)

    def test_get_doctor(self):
        result = self.client.get('/api/doctors/9')
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertTrue('id' in result.json)

    def test_get_doctor_error(self):
        result = self.client.get('/api/doctors/9999')
        self.assertEqual(404, result.status_code)

        result = self.client.get('/api/doctors/test')
        self.assertEqual(404, result.status_code)


if __name__ == '__main__':
    unittest.main()
