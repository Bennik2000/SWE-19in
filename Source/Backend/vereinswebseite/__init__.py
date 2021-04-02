from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask("VereinSWEbseite",
            template_folder="vereinswebseite/templates",
            static_url_path='',
            static_folder='vereinswebseite/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

# Ignore PEP8 this one time to have the routes in a separate file,
# while avoiding circular imports
from vereinswebseite import routes  # noqa: E402
from vereinswebseite import routes_users  # noqa: E402
from vereinswebseite import routes_articles  # noqa: E402
from vereinswebseite import routes_static  # noqa: E402
