from unittest import TestCase
from vereinswebseite import app, db
from copy import deepcopy
from http import HTTPStatus
from vereinswebseite.models import User

from vereinswebseite.models import AccessToken


class UserLoginSessionTest(TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    ValidAccessToken = "VALID_TOKEN"

    ValidTestJson = {
        "name": TestUserName,
        "email": TestEmail,
        "password": TestPassword,
        "token": ValidAccessToken
    }

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        # app.config["SQLALCHEMY_ECHO"] = True
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_delete_user(self):
        self.app.post("/users", json=self.ValidTestJson)
        self.app.post("/users/login", json=self.ValidTestJson)
        response = self.app.delete("/users/delete")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(db.session.query(User.name).filter_by(name='TestUser').first())

    def test_register_user_valid_user(self):
        self._prepare_access_token()
        response = self.app.post("/users", json=self.ValidTestJson)
        print(f"JSON response: {response.json}")
        self.assertTrue(response.json.items() >= {"success": True}.items())
        self._assert_access_token_deleted()

    def test_register_user_existing_user(self):
        response = None
        for i in range(2):
            self._prepare_access_token()
            response = self.app.post("/users", json=self.ValidTestJson)
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
        response = self.app.post("/users", json=invalid_json)
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
