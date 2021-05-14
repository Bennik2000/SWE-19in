from http import HTTPStatus
from test.base_test_case import BaseTestCase, TestUserName, TestEmail, TestPassword
from vereinswebseite.models.user import User


class UserRolesTest(BaseTestCase):
    def test_given_user_was_assigned_role_then_has_roles_returns_true(self):
        user = self.create_and_login_test_user(roles=['Webmaster', 'Vorstand'])

        self.assertTrue(user.has_roles('Webmaster', 'Vorstand'))

    def test_given_first_user_created_then_user_is_webmaster(self):
        user_registration_json = {
            "name": TestUserName,
            "email": TestEmail,
            "password": TestPassword,
            "token": "TOKEN"
        }

        self.app.post("/api/users", json=user_registration_json)

        user = User.query.filter_by(email=TestEmail).first()

        self.assertTrue(user.has_roles('Webmaster'),
                        "First created user is not the webmaster")

    def test_given_add_roles_with_set_user_roles_then_user_has_roles(self):
        user = self.create_and_login_test_user(roles=['Webmaster'])

        response = self.app.put(
            "/api/users/user_roles",
            json={
                "user_id": user.id,
                "roles": ['Vorstand', ]
            }
        )

        self.assertTrue(response.json["success"], f"Unexpected JSON response: {response.json}")
        self.assertTrue(user.has_roles('Vorstand'), 'User does not have the expected role')

    def test_given_role_removed_then_user_doesnt_have_role(self):
        user = self.create_and_login_test_user(roles=['Webmaster', 'Vorstand'])

        response = self.app.put(
            "/api/users/user_roles",
            json={
                "user_id": user.id,
                "roles": ['Webmaster', ]
            }
        )

        self.assertTrue(response.json["success"], f"Unexpected JSON response: {response.json}")
        self.assertFalse(user.has_roles('Vorstand'), 'User still has the role which should have been removed')

    def test_given_invalid_user_id_on_set_user_roles_then_error(self):
        self.create_and_login_test_user(roles=['Webmaster'])

        response = self.app.put(
            "/api/users/user_roles",
            json={
                "user_id": -1,
                "roles": ['Vorstand', ]
            }
        )

        print(f"JSON response: {response.json}")
        self.assertFalse(response.json["success"], f"Unexpected JSON response: {response.json}")

    def test_given_invalid_role_on_set_user_roles_then_error(self):
        user = self.create_and_login_test_user(roles=['Webmaster'])

        response = self.app.put(
            "/api/users/user_roles",
            json={
                "user_id": user.id,
                "roles": ['Vorstand', 'InvalidRoleName']
            }
        )

        print(f"JSON response: {response.json}")
        self.assertFalse(response.json["success"], f"Unexpected JSON response: {response.json}")

    def test_given_get_user_roles_then_correct_roles_returned(self):
        test_user_roles = ['Webmaster', 'Vorstand']
        user = self.create_and_login_test_user(roles=test_user_roles)

        response = self.app.get(
            "/api/users/user_roles",
            json={
                "user_id": user.id
            }
        )

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["success"], f"Expected success to be true")
        self.assertEqual(response.json["roles"], test_user_roles)

    def test_given_not_webmaster_on_get_user_roles_then_unauthorized(self):
        user = self.create_and_login_test_user()

        response = self.app.get(
            "/api/users/user_roles",
            json={
                "user_id": user.id
            }
        )

        self.assertFalse(response.json["success"], f"Unexpected JSON response: {response.json}")
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_given_get_current_user_roles_then_correct_roles_returned(self):
        test_user_roles = ['Vorstand']
        self.create_and_login_test_user(roles=test_user_roles)

        response = self.app.get("/api/users/current_user_roles")

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["success"], f"Expected success to be true")
        self.assertEqual(response.json["roles"], test_user_roles)

    def test_given_webmaster_on_get_users_then_correct_roles_received(self):
        test_user_roles = ['Webmaster', 'Vorstand']
        user = self.create_and_login_test_user(roles=test_user_roles)

        response = self.app.get("/api/users")

        print(f"JSON response: {response.json}")
        self.assertEqual(len(response.json), 1, "Response contains more users than expected")
        roles_received = response.json[0].get('roles')
        self.assertIsNotNone(roles_received, "No roles received")
        self.assertEqual(roles_received, test_user_roles)
