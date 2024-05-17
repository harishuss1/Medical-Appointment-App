import json
import datetime
import unittest
from MedicalApp import create_app
from MedicalApp.user import User, MedicalPatient
from MedicalApp.note import Note


class TestNoteAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()
        
    def test_addnote_success_201(self):
        data = {
        }
        data['patient_id'] = 7
        data['note_taker_id'] = 9
        data['note_date'] = "2024-07-22"
        data['note'] = "Test Note"
        data['attachment_paths'] = "/attachments/attachment1.pdf"
        json_string = json.dumps(data)
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.put('/api/notes/', data=json_string, headers=headers, content_type='application/json')
        self.assertEqual(201, result.status_code)
        self.assertNotEqual("", result.headers['Note'])
        self.assertNotEqual(9, result.headers['Note'].split("/")[-1])
    

if __name__ == '__main__':
    unittest.main()