from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

# Run App
if __name__ == '__main__':
    app.run(debug=True)
