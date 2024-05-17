import unittest
from MedicalApp import create_app


class TestNoteAPI(unittest.TestCase):
    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    # def test_get_notes(self):
    #     result = self.client.get('/api/notes/')
    #     self.assertEqual(200, result.status_code)
    #     self.assertIsNotNone(result.json)
    #     self.assertTrue('count' in result.json)

    # def test_get_note_by_id(self):
    #     result = self.client.get('/api/notes/1')
    #     self.assertEqual(200, result.status_code)
    #     self.assertIsNotNone(result.json)
    #     self.assertTrue('id' in result.json)

    # def test_get_note_by_id_not_found(self):
    #     result = self.client.get('/api/notes/9999')
    #     self.assertEqual(404, result.status_code)

    # def test_get_note_by_id_invalid_id(self):
    #     result = self.client.get('/api/notes/test')
    #     self.assertEqual(400, result.status_code)


if __name__ == '__main__':
    unittest.main()