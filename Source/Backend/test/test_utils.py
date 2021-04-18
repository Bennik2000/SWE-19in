from vereinswebseite import limiter, app, db


def setup_test_app(limiter_enabled = False):
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    db.drop_all()
    db.create_all()

    limiter.enabled = limiter_enabled

    return app.test_client()
