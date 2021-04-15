import jinja2

from vereinswebseite import limiter, app, db
import vereinswebseite
from vereinswebseite.models import User


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


def add_test_user(test_user_name, test_email, test_password):
    user = User(name=test_user_name, email=test_email)
    user.set_password(test_password)
    db.session.add(user)
    db.session.commit()


def create_and_login_test_user(test_app, test_user_name, test_email, test_password):
    add_test_user(test_user_name, test_email, test_password)
    test_app.post("/users/login", json={
        "email": test_email,
        "password": test_password
    })
