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
    
    def test_change_email_request_not_logged_in(self):
        response: Response = self.app.post("/users/change_email")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_email_valid(self):
        self._create_and_login_testuser()
        neueEmail = "test@mcfly.de"
        self.app.post("/users/change_email", json={
            "email": neueEmail
        })
        self.assertIsNotNone(User.query.filter_by(email=neueEmail).first())
       
       
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
