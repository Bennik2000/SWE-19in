import datetime

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

app = Flask("VereinSWEbseite",
            template_folder="vereinswebseite/templates",
            static_url_path='',
            static_folder='vereinswebseite/static')

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "M2JjYjU2NDZmYzUJhMIgIC0K"
app.config["REMEMBER_COOKIE_DURATION"] = datetime.timedelta(weeks=12)
app.config['JSON_AS_ASCII'] = False
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'vereinSWEbseite@gmail.com'
app.config['MAIL_PASSWORD'] = '2021SWEsem4'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "60 per hour"]
)

db = SQLAlchemy(app)
ma = Marshmallow(app)
login_manager = LoginManager(app)

# Ignore PEP8 this one time to have the routes in a separate file,
# while avoiding circular imports
from vereinswebseite import routes  # noqa: E402
from vereinswebseite import routes_users  # noqa: E402
from vereinswebseite import routes_accss_token  # noqa: E402
from vereinswebseite import routes_blog_posts  # noqa: E402
from vereinswebseite import routes_static  # noqa: E402

db.create_all()
