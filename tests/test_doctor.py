import unittest
from MedicalApp import create_app
from MedicalApp.user import User


class UserTestCases(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.update({"TESTING": True})
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_create_user_successful(self):
        user = User("user@domain.com", "password", "John",
                    "Doe", "STAFF", "/path/to/avatar.png", 1)
        self.assertEqual("user@domain.com", user.email)
        self.assertEqual("password", user.password)
        self.assertEqual("John", user.first_name)
        self.assertEqual("Doe", user.last_name)
        self.assertEqual("STAFF", user.access_level)
        self.assertEqual("/path/to/avatar.png", user.avatar_path)
        self.assertEqual(1, user.id)

    def test_create_user_bad_email(self):
        with self.assertRaises(ValueError):
            User(123, "password", "John", "Doe",
                 "STAFF", "/path/to/avatar.png", 1)

    def test_create_user_bad_password(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", 123, "John", "Doe",
                 "STAFF", "/path/to/avatar.png", 1)

    def test_create_user_bad_first_name(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", "password", 123,
                 "Doe", "STAFF", "/path/to/avatar.png", 1)

    def test_create_user_bad_last_name(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", "password", "John",
                 123, "STAFF", "/path/to/avatar.png", 1)

    def test_create_user_bad_access_level(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", "password", "John",
                 "Doe", 123, "/path/to/avatar.png", 1)

    def test_create_user_bad_avatar_path(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", "password", "John", "Doe", "STAFF", 123, 1)

    def test_create_user_bad_id(self):
        with self.assertRaises(ValueError):
            User("user@domain.com", "password", "John",
                 "Doe", "STAFF", "/path/to/avatar.png", "1")


if __name__ == '__main__':
    unittest.main()
