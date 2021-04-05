from unittest import TestCase
from vereinswebseite import app, db
from copy import deepcopy


class UserLoginSessionTest(TestCase):
    TestUserName = "TestUser"
    TestEmail = "test@email.com"
    TestPassword = "TestPassword"

    ValidTestJson = {
        "name": TestUserName,
        "email": TestEmail,
        "password": TestPassword
    }

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        #app.config["SQLALCHEMY_ECHO"] = True
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_register_user_valid_user(self):
        response = self.app.post("/users", json=self.ValidTestJson)
        print(f"JSON response: {response.json}")
        self.assertTrue(response.json.items() >= {"success": True}.items())

    def test_register_user_existing_user(self):
        response = None
        for i in range(2):
            response = self.app.post("/users", json=self.ValidTestJson)
        print(f"JSON response: {response.json}")
        self._assert_user_not_registered_and_error(response)

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
        response = self.app.post("/users", json=invalid_json)
        print(f"JSON response: {response.json}")
        self._assert_user_not_registered_and_error(response)

    def _assert_user_not_registered_and_error(self, response):
        self.assertTrue(response.json.items() >= {"success": False}.items())
        self.assertIsNotNone(response.json.get("errors"))
