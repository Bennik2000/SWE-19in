from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask("VereinSWEbseite")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Ignore PEP8 this one time to have the routes in a separate file,
# while avoiding circular imports
from vereinswebseite import routes  # noqa: E402
