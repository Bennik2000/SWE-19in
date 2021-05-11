import unittest
from http import HTTPStatus
from werkzeug import Response

from test.base_test_case import BaseTestCase, TestUserName, TestEmail


class UserPersonalInfoTest(BaseTestCase):
    def test_personal_info_request_resource_found(self):
        response: Response = self.app.get("/api/users/personal_info")
        self.assertNotEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_not_logged_in_unauthorized(self):
        response: Response = self.app.get("/api/users/personal_info")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_logged_in_response_ok(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        self.assertEqual(response.status_code, HTTPStatus.OK)
        print(f"JSON response: {response.json}")

    def test_logged_in_response_not_empty(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        self.assertNotEqual(response.json, {})
        print(f"JSON response: {response.json}")

    def test_logged_in_only_one_user_received(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        self.assertNotIsInstance(response.json, list)
        self.assertIsInstance(response.json, dict)

    def test_logged_in_current_user_email_received(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        user_email = response.json.get("email")
        self.assertIsNotNone(user_email)
        self.assertEqual(user_email, TestEmail)

    def test_logged_in_current_user_name_received(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        user_name = response.json.get("name")
        self.assertIsNotNone(user_name)
        self.assertEqual(user_name, TestUserName)

    def test_logged_in_current_roles_received(self):
        test_user_roles = ['Vorstand']
        self.create_and_login_test_user(roles=test_user_roles)
        response: Response = self.app.get("/api/users/personal_info")
        roles_received = response.json.get("roles")
        self.assertIsNotNone(roles_received, "No roles received")
        self.assertEqual(roles_received, test_user_roles)
        print(f"JSON response: {response.json}")

    def test_logged_in_password_not_sent(self):
        self.create_and_login_test_user()
        response: Response = self.app.get("/api/users/personal_info")
        user_password = response.json.get("password")
        self.assertIsNone(user_password)


if __name__ == '__main__':
    unittest.main()
