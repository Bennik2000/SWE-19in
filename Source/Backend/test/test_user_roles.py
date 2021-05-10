from vereinswebseite.models import Role, User

from base_test_case import BaseTestCase, TestUserName, TestEmail, TestPassword


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


def _get_webmaster_role():
    return Role.query.filter_by(name='Webmaster').first()


def _get_vorstand_role():
    return Role.query.filter_by(name='Vorstand').first()
