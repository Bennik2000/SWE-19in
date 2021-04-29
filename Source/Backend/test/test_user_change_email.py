import unittest
from http import HTTPStatus
from werkzeug import Response
from vereinswebseite import app, db, login_manager
from vereinswebseite.models import User
from flask_login import current_user
from test.test_utils import setup_test_app, create_and_login_test_user, TestUserName, TestEmail



class UserChangeEmailTest(unittest.TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    def setUp(self) -> None:
        app.config["TESTING"] = True
        self.app = setup_test_app()
    
    def test_change_email_request_not_logged_in(self):
        response: Response = self.app.post("/users/change_email")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_email_valid(self):
        create_and_login_test_user(self.app)
        neueEmail = "test@mcfly.de"
        self.app.post("/users/change_email", json={
            "email": neueEmail
        })
        self.assertIsNotNone(User.query.filter_by(email=neueEmail).first())
       
       
   

   