import unittest
from MedicalApp import create_app


class MedicalTestCases(unittest.TestCase):
    def setUp(self):
        app = create_app(test_config={})
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_dummy(self):
        test = "dummy"
        self.assertEqual("dummy", test)


if __name__ == '__main__':
    unittest.main()
