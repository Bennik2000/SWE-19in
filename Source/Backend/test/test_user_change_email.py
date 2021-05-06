import unittest
from http import HTTPStatus
from werkzeug import Response
from vereinswebseite import app
from vereinswebseite.models import User
from test.test_utils import setup_test_app, create_and_login_test_user


class UserChangeEmailTest(unittest.TestCase):
    def setUp(self) -> None:
        app.config["TESTING"] = True
        self.app = setup_test_app()
    
    def test_change_email_request_not_logged_in(self):
        response: Response = self.app.post("/api/users/change_email")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_email_valid(self):
        create_and_login_test_user(self.app)
        new_email = "test@mcfly.de"
        self.app.post("/api/users/change_email", json={
            "email": new_email
        })
        self.assertIsNotNone(User.query.filter_by(email=new_email).first())
