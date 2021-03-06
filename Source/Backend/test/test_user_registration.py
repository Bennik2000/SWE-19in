from test.base_test_case import BaseTestCase, TestUserName, TestEmail, TestPassword
from copy import deepcopy
from http import HTTPStatus

from vereinswebseite.models import db
from vereinswebseite.models.token import AccessToken
from vereinswebseite.models.user import User


class UserRegistrationTest(BaseTestCase):
    ValidAccessToken = "VALID_TOKEN"

    ValidTestJson = {
        "name": TestUserName,
        "email": TestEmail,
        "password": TestPassword,
        "token": ValidAccessToken
    }

    def test_delete_user(self):
        self._prepare_access_token()
        self.app.post("/api/users", json=self.ValidTestJson)
        self.app.post("/api/users/login", json=self.ValidTestJson)
        response = self.app.delete("/api/users/delete")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(db.session.query(User.name).filter_by(name='TestUser').first())

    def test_login_user_email_case_insensitive(self):
        self._prepare_access_token()
        self.app.post("/api/users", json=self.ValidTestJson)
        self.app.post("/api/users/logout")

        response = self.app.post("/api/users/login", json={
            "email": TestEmail.upper(),
            "password": TestPassword
        })

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(response.json["success"])

    def test_register_user_valid_user(self):
        self._prepare_access_token()
        response = self.app.post("/api/users", json=self.ValidTestJson)
        print(f"JSON response: {response.json}")
        self.assertTrue(response.json.items() >= {"success": True}.items())
        self._assert_access_token_deleted()

    def test_register_user_existing_user(self):
        response = None
        for i in range(2):
            self._prepare_access_token()
            response = self.app.post("/api/users", json=self.ValidTestJson)
        print(f"JSON response: {response.json}")
        self._assert_user_not_registered_and_error(response)
        self._assert_access_token_not_deleted()

    def test_register_user_name_missing(self):
        invalid_json = deepcopy(self.ValidTestJson)
        del invalid_json["name"]
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_name_null(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["name"] = None  # noqa
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_name_empty(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["name"] = ""
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_email_missing(self):
        invalid_json = deepcopy(self.ValidTestJson)
        del invalid_json["email"]
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_email_null(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["email"] = None  # noqa
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_email_empty(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["email"] = ""
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_password_missing(self):
        invalid_json = deepcopy(self.ValidTestJson)
        del invalid_json["password"]
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_password_null(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["password"] = None  # noqa
        self._send_invalid_json_and_assert_error(invalid_json)

    def test_register_user_password_empty(self):
        invalid_json = deepcopy(self.ValidTestJson)
        invalid_json["password"] = ""
        self._send_invalid_json_and_assert_error(invalid_json)

    def _send_invalid_json_and_assert_error(self, invalid_json):
        self._prepare_access_token()
        response = self.app.post("/api/users", json=invalid_json)
        print(f"JSON response: {response.json}")
        self._assert_user_not_registered_and_error(response)
        self._assert_access_token_not_deleted()

    def _assert_user_not_registered_and_error(self, response):
        self.assertTrue(response.json.items() >= {"success": False}.items())
        self.assertIsNotNone(response.json.get("errors"))

    def _prepare_access_token(self):
        db.session.add(AccessToken(self.ValidAccessToken))
        db.session.commit()

    def _assert_access_token_deleted(self):
        self.assertIsNone(AccessToken.query.get(self.ValidAccessToken))

    def _assert_access_token_not_deleted(self):
        self.assertIsNotNone(AccessToken.query.get(self.ValidAccessToken))
