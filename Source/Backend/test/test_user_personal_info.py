import unittest
from http import HTTPStatus
from werkzeug import Response

from test.test_utils import setup_test_app
from vereinswebseite import db
from vereinswebseite.models import User


class UserPersonalInfoTest(unittest.TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    def setUp(self) -> None:
        self.app = setup_test_app()

    def test_personal_info_request_resource_found(self):
        response: Response = self.app.get("/users/personal_info")
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_not_logged_in_unauthorized(self):
        response: Response = self.app.get("/users/personal_info")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_logged_in_response_ok(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(f"JSON response: {response.json}")

    def test_logged_in_response_not_empty(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        self.assertNotEqual(response.json, {})
        print(f"JSON response: {response.json}")

    def test_logged_in_only_one_user_received(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        self.assertNotIsInstance(response.json, list)
        self.assertIsInstance(response.json, dict)

    def test_logged_in_current_user_email_received(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        user_email = response.json.get("email")
        self.assertIsNotNone(user_email)
        self.assertEqual(user_email, self.TestEmail)

    def test_logged_in_current_user_name_received(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        user_name = response.json.get("name")
        self.assertIsNotNone(user_name)
        self.assertEqual(user_name, self.TestUserName)

    def test_logged_in_password_not_sent(self):
        self._create_and_login_testuser()
        response: Response = self.app.get("/users/personal_info")
        user_password = response.json.get("password")
        self.assertIsNone(user_password)

    def _create_and_login_testuser(self):
        self._add_testuser()
        self.app.post("/users/login", json={
            "email": self.TestEmail,
            "password": self.TestPassword
        })

    def _add_testuser(self):
        user = User(name=self.TestUserName, email=self.TestEmail)
        user.set_password(self.TestPassword)
        db.session.add(user)
        db.session.commit()


if __name__ == '__main__':
    unittest.main()
