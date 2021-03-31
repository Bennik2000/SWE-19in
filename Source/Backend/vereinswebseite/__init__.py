import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager


app = Flask("VereinSWEbseite")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "M2JjYjU2NDZmYzUJhMIgIC0K"
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(weeks=12)

db = SQLAlchemy(app)
ma = Marshmallow(app)
login_manager = LoginManager(app)

# Ignore PEP8 this one time to have the routes in a separate file,
# while avoiding circular imports
from vereinswebseite import routes  # noqa: E402
from vereinswebseite import routes_users  # noqa: E402
from vereinswebseite import routes_articles  # noqa: E402

db.create_all()
