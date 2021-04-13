import unittest
from http import HTTPStatus
from werkzeug import Response
from vereinswebseite import app, db, login_manager
from vereinswebseite.models import User
from flask_login import current_user


class UserChangePasswordTest(unittest.TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
    
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
