import unittest

from flask import json
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
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/medical_rooms', headers=headers)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertEqual(1, len(result.json))

    def test_get_medical_room_by_room_number(self):
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/medical_rooms/101', headers=headers)
        self.assertEqual(200, result.status_code)
        self.assertIsNotNone(result.json)
        self.assertEqual("101", result.json['room_number'])

    def test_get_medical_room_by_invalid_room_number(self):
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/medical_rooms/1000', headers=headers)
        self.assertEqual(404, result.status_code)
        
    def test_createmedicalroom_successful(self):
        data = {}
        data['room_number'] = '118'
        data['description'] = "yayyy!"
        json_string = json.dumps(data)
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/medical_rooms', headers=headers, data=json_string, content_type='application/json')
        self.assertEqual(201, result.status_code)
        result = result.json
        self.assertEqual("118", result['room_number'])
        
    def test_createmedicalroom_medicalroomexists(self):
        data = {}
        data['room_number'] = '105'
        data['description'] = "yayyy!"
        json_string = json.dumps(data)
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/medical_rooms', headers=headers, data=json_string, content_type='application/json')
        response_data = json.loads(result.get_data(as_text=True))
        self.assertEqual(400, result.status_code)
        self.assertEqual("The room you have provided already exists", response_data['description'])
        
    def test_createmedicalroom_nodescription(self):
        data = {}
        data['room_number'] = '105'
        json_string = json.dumps(data)
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/medical_rooms', headers=headers, data=json_string, content_type='application/json')
        response_data = json.loads(result.get_data(as_text=True))
        self.assertEqual(400, result.status_code)
        self.assertEqual("No room number or description parameter found.", response_data['description'])
        
    def test_createmedicalroom_roomempty(self):
        data = {}
        data['room_number'] = ""
        data['description'] = "blahhhh"
        json_string = json.dumps(data)
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/medical_rooms', headers=headers, data=json_string, content_type='application/json')
        response_data = json.loads(result.get_data(as_text=True))
        self.assertEqual(400, result.status_code)
        self.assertEqual("Empty room number or description params.", response_data['description'])
        
    def test_createmedicalroom_descriptionempty(self):
        data = {}
        data['room_number'] = "118"
        data['description'] = ""
        json_string = json.dumps(data)
        token = "ErU49l4Du_LEvsV1AgU9SIllZ1g"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/medical_rooms', headers=headers, data=json_string, content_type='application/json')
        response_data = json.loads(result.get_data(as_text=True))
        self.assertEqual(400, result.status_code)
        self.assertEqual("Empty room number or description params.", response_data['description'])



if __name__ == '__main__':
    unittest.main()

