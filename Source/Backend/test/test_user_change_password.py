import unittest
from http import HTTPStatus
from werkzeug import Response

from base_test_case import BaseTestCase, TestEmail
from vereinswebseite.models import User


class UserChangePasswordTest(BaseTestCase):
    def test_change_password_request_not_logged_in(self):
        response: Response = self.app.post("/api/users/change_password")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_password_valid(self):
        self.create_and_login_test_user()
        new_password = "newPassword"
        self.app.post("/api/users/change_password", json={
            "password": new_password
        })
        existing_user = User.query.filter_by(email=TestEmail).first()
        self.assertTrue(existing_user.check_password(new_password))


if __name__ == '__main__':
    unittest.main()
