import datetime

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "M2JjYjU2NDZmYzUJhMIgIC0K"
REMEMBER_COOKIE_DURATION = datetime.timedelta(weeks=12)
JSON_AS_ASCII = False
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'vereinSWEbseite@gmail.com'
MAIL_PASSWORD = '2021SWEsem4'
MAIL_USE_TLS = False
MAIL_USE_SSL = True

SERVER_HOSTNAME = "127.0.0.1"
SERVER_PATH = "/"

ROLES = ["Webmaster", "Vorstand"]
