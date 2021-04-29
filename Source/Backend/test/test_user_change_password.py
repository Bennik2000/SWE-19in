import unittest
from http import HTTPStatus
from werkzeug import Response

from test.test_utils import setup_test_app, create_and_login_test_user, TestEmail
from vereinswebseite import db
from vereinswebseite.models import User


class UserChangePasswordTest(unittest.TestCase):
    def setUp(self) -> None:
        self.app = setup_test_app()
    
    def test_change_password_request_not_logged_in(self):
        response: Response = self.app.post("/api/users/change_password")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_password_valid(self):
        create_and_login_test_user(self.app)
        newPassword = "newPassword"
        self.app.post("/api/users/change_password", json={
            "password": newPassword
        })
        existing_user = User.query.filter_by(email=TestEmail).first()
        self.assertTrue(existing_user.check_password(newPassword))


if __name__ == '__main__':
    unittest.main()
