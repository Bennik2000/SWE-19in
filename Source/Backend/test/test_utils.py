import jinja2
import os

from vereinswebseite import limiter, app, db
import vereinswebseite
from vereinswebseite.models import User


TestUserName = "TestUser"
TestEmail = "test@email.com"
TestPassword = "TestPassword"


def setup_test_app(limiter_enabled=False, email_enabled=False):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    app.jinja_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['../vereinswebseite/templates']),
    ])

    db.drop_all()
    db.create_all()

    limiter.enabled = limiter_enabled

    if not email_enabled:
        vereinswebseite.mail = None

    return app.test_client()


def add_test_user() -> User:
    test_user = User(name=TestUserName, email=TestEmail)
    test_user.set_password(TestPassword)
    db.session.add(test_user)
    db.session.commit()
    return test_user


def create_and_login_test_user(test_app) -> User:
    test_user = add_test_user()
    test_app.post("/api/users/login", json={
        "email": TestEmail,
        "password": TestPassword
    })

    return test_user
