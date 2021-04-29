import unittest
from http import HTTPStatus

from test.test_utils import setup_test_app, add_test_user, TestEmail
from vereinswebseite import db
from vereinswebseite.models import PasswordResetToken, User


class UserPasswordResetTest(unittest.TestCase):
    TestToken = "ZHHEU2345"

    def setUp(self) -> None:
        self.app = setup_test_app()
        add_test_user()

    def test_given_user_exists_when_request_password_reset_then_token_generated(self):
        self.clear_reset_tokens()
        response = self.app.post("/api/users/request_new_password", json={"email": TestEmail})

        self.assertTrue(response.json["success"])
        self.assertEqual(len(PasswordResetToken.query.all()), 1)

    def test_given_user_not_exists_when_request_password_reset_then_no_token(self):
        self.clear_reset_tokens()
        response = self.app.post("/api/users/request_new_password", json={"email": "NotExisting"})

        self.assertTrue(response.json["success"])
        self.assertEqual(len(PasswordResetToken.query.all()), 0)

    def test_given_correct_token_when_reset_password_then_success(self):
        self.insert_test_token()

        response = self.app.get("/users/reset_password/" + self.TestToken)
        self.assertTrue(response.status, HTTPStatus.OK)

    def test_given_incorrect_token_when_reset_password_then_not_found(self):
        self.insert_test_token()

        response = self.app.get("/users/reset_password/" + "invalidToken")
        self.assertTrue(response.status, HTTPStatus.NOT_FOUND)

    def test_given_correct_token_when_reset_password_then_new_password_set(self):
        self.insert_test_token()

        new_password = "newPassword"
        response = self.app.post("/api/users/reset_password", json={
            "password": new_password,
            "token": self.TestToken})

        self.assertTrue(response.json["success"])
        self.assertTrue(self.check_password(TestEmail, new_password))
        self.assertIsNone(PasswordResetToken.query.get(self.TestToken))

    def test_given_incorrect_token_when_reset_password_then_new_password_not_set(self):
        self.insert_test_token()

        new_password = "newPassword"
        response = self.app.post("/api/users/reset_password", json={
            "password": new_password,
            "token": "invalidToken"})

        self.assertFalse(response.json["success"])
        self.assertFalse(self.check_password(TestEmail, new_password))
        self.assertIsNotNone(PasswordResetToken.query.get(self.TestToken))

    def insert_test_token(self):
        user = User.query.filter_by(email=TestEmail).first()
        token = PasswordResetToken(self.TestToken, user)

        db.session.add(token)
        db.session.commit()

    @staticmethod
    def clear_reset_tokens():
        PasswordResetToken.query.delete()

    @staticmethod
    def check_password(email, password):
        user = User.query.filter_by(email=email).first()
        return user.check_password(password)
