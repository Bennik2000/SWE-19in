from vereinswebseite import app, db
from vereinswebseite.models import User
from flask import request


@app.route('/')
def index():
    return 'Hello, World!'


# Create User Data
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    new_user = User(name, email, password)
    try:
        db.session.add(new_user)
        db.session.commit()
        return 201
    except Exception:
        return Exception.args
