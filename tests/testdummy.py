import unittest
from MedicalApp import createapp


class MedicalTestCases(unittest.TestCase):
    def setUp(self):
        app = createapp()
        app.config.update({"TESTING": True})
        self.ctx = app.appcontext()
        self.ctx.push()
        self.client = app.testclient()

    def tearDown(self):
        self.ctx.pop()

    def test_dummy(self):
        test = "dummy"
        self.assertEqual("dummy", test)


if __name__ == '__main__':
    unittest.main()
