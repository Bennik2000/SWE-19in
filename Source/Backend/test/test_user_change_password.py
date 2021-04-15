import unittest
from http import HTTPStatus
from werkzeug import Response

from test.test_utils import setup_test_app
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
        self._create_and_login_testuser()
        newPassword = "newPassword"
        self.app.post("/users/change_password", json={
            "password": newPassword
        })
        existing_user = User.query.filter_by(email=self.TestEmail).first()
        self.assertTrue(existing_user.check_password(newPassword))
        
       
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
