from vereinswebseite import app, db
from vereinswebseite.models import User, UserSchema
from flask import request, jsonify

# Init Schemas
OneUser = UserSchema()
ManyUsers = UserSchema(many=True)

# Create User
@app.route('/user', methods=['POST'])
def add_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']
    new_user = User(name, email, password)

    db.session.add(new_user)
    db.session.commit()
    return "User " + name + " Added"


# Get all Users
@app.route('/user', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = jsonify(ManyUsers.dump(all_users))
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


# Get one Users
@app.route('/user/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    result = OneUser.jsonify(user)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result
