from unittest import TestCase
import jinja2
import vereinswebseite
from vereinswebseite.models import db
from vereinswebseite.models.roles import Role
from vereinswebseite.models.user import User

TestUserName = "TestUser"
TestEmail = "test@email.com"
TestPassword = "TestPassword"


class BaseTestCase(TestCase):
    def setUp(self, custom_config=None, limiter_enabled=False, email_enabled=False):
        unittesting_config = {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "RATELIMIT_ENABLED": limiter_enabled
        }

        if custom_config is not None:
            unittesting_config |= custom_config

        self.flask_app = vereinswebseite.create_app(unittesting_config)

        self.flask_app.jinja_loader = jinja2.ChoiceLoader([
            self.flask_app.jinja_loader,
            jinja2.FileSystemLoader(['../vereinswebseite/templates']),
        ])

        if not email_enabled:
            vereinswebseite.mail = None

        self.app_context = self.flask_app.app_context()
        self.app_context.push()
        self.app = self.flask_app.test_client()

        db.drop_all()
        vereinswebseite.init_db()

    def tearDown(self):
        self.app_context.pop()

    def add_test_user(self, roles=None) -> User:
        test_user = User(name=TestUserName, email=TestEmail)
        test_user.set_password(TestPassword)

        if roles is not None:
            test_user.roles = [Role.query.filter_by(name=role_name).first() for role_name in roles]

        db.session.add(test_user)
        db.session.commit()
        return User.query.filter_by(email=TestEmail).first()

    def create_and_login_test_user(self, roles=None) -> User:
        self.add_test_user(roles=roles)
        self.app.post("/api/users/login", json={
            "email": TestEmail,
            "password": TestPassword
        })

        return User.query.filter_by(email=TestEmail).first()