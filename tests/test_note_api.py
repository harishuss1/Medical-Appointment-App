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
        data['attachment_paths'] = ["/attachments/attachment1.pdf"]
        json_string = json.dumps(data)
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.post('/api/notes/', data=json_string, headers=headers, content_type='application/json')
        self.assertEqual(201, result.status_code)
        self.assertNotEqual("", result.json)
        self.assertEqual("Test Note", result.json["note"])
    
    
    #(Note(patient=self.patients[0], note_taker=self.users[3], note_date=datetime.date(2024,5,30), note='Follow-up examination conducted. Patient reports improvement in condition. Continuing current medication.', attachement_path=["/attachments/attachments1.pdf"],id=1))
    
    def test_getnotes_page_success(self):
        token = "mIzbZLyEzNKW7SP5NAx9eUHUq_w"
        headers = {'Authorization': f'Bearer {token}'}
        result = self.client.get('/api/notes', headers=headers)
        self.assertEqual(200, result.status_code)
        results = result.json['results']
        self.assertIsNotNone(results)
        self.assertEqual(2, len(results))
        self.assertEqual("Follow-up examination conducted. Patient reports improvement in condition. Continuing current medication.", results[0]['note'])
        self.assertEqual(["/attachments/attachments1.pdf"], results[0]['attachment_path'])
        self.assertEqual(1, results[0]['id'])
    

if __name__ == '__main__':
    unittest.main()