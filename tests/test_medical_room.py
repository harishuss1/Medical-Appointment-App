import unittest
from MedicalApp import create_app
from MedicalApp.medical_room import MedicalRoom
from MedicalApp.db.fake_db import FakeDB

class MedicalRoomConstructorTest(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_constructor_valid_values(self):
        room = MedicalRoom("101", "test1")
        self.assertEqual("101", room.room_number)
        self.assertEqual("test1", room.description)

    def test_constructor_invalid_room_number(self):
        with self.assertRaises(ValueError):
            MedicalRoom(None, "test1")

        with self.assertRaises(ValueError):
            MedicalRoom(101, "test1")

    def test_constructor_invalid_description(self):
        with self.assertRaises(ValueError):
            MedicalRoom("101", None)

        with self.assertRaises(ValueError):
            MedicalRoom("101", 101)

    def test_get_medical_rooms(self):
        result = self.client.get('/api/medical_rooms/')
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertEqual(1, len(result.json))

    def test_get_medical_room_by_room_number(self):
        result = self.client.get('/api/medical_rooms/101')
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertEqual("101", result.json['room_number'])

    def test_get_medical_room_by_invalid_room_number(self):
        result = self.client.get('/api/medical_rooms/1000')
        self.assertEqual(404, result.status_code)

if __name__ == '__main__':
    unittest.main()

