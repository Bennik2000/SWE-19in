import unittest
from http import HTTPStatus
from werkzeug import Response

from test.test_utils import setup_test_app, create_and_login_test_user
from vereinswebseite import db
from vereinswebseite.models import User


class UserChangePasswordTest(unittest.TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    def setUp(self) -> None:
        self.app = setup_test_app()
    
    def test_change_password_request_not_logged_in(self):
        response: Response = self.app.post("/users/change_password")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_password_valid(self):
        create_and_login_test_user(self.app, self.TestUserName, self.TestEmail, self.TestPassword)
        newPassword = "newPassword"
        self.app.post("/users/change_password", json={
            "password": newPassword
        })
        existing_user = User.query.filter_by(email=self.TestEmail).first()
        self.assertTrue(existing_user.check_password(newPassword))


if __name__ == '__main__':
    unittest.main()
