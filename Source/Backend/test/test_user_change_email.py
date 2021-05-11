import unittest
from http import HTTPStatus
from werkzeug import Response
from vereinswebseite.models import User
from test.base_test_case import BaseTestCase


class UserChangeEmailTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp(custom_config={
            "TESTING": True
        })
    
    def test_change_email_request_not_logged_in(self):
        response: Response = self.app.post("/api/users/change_email")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
    
    def test_logged_in_change_email_valid(self):
        self.create_and_login_test_user()

        new_email = "test@mcfly.de"
        self.app.post("/api/users/change_email", json={
            "email": new_email
        })

        self.assertIsNotNone(User.query.filter_by(email=new_email).first())
