from vereinswebseite import app, db
from vereinswebseite.models import User, AccessCode, UserSchema, AccessCodeSchema
from flask import request, jsonify
from uuid import uuid4


# Init Schemas
OneUser = UserSchema()
ManyUsers = UserSchema(many=True)

OneAccessCode = AccessCodeSchema()
ManyAccessCode = AccessCodeSchema(many=True)

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


@app.route('/accessCode/validate/<code>')
def validate_access_code(code):
    access_code = AccessCode.query.get(code)

    if not access_code:
        return "No access :(", 403
    else:
        return "Access granted", 200


@app.route('/accessCode/delete/<code>')
def delete_access_code(code):
    access_code = AccessCode.query.get(code)

    if not access_code:
        return "Access code not found", 404

    db.session.delete(access_code)
    db.session.commit()
    return "Success", 200


@app.route('/accessCode/create')
def create_access_code():
    access_code = str(uuid4())[0:8].upper()
    code = AccessCode(access_code)

    db.session.add(code)
    db.session.commit()

    return OneAccessCode.jsonify(code)


@app.route('/accessCode', methods=['GET'])
def all_access_code():
    all_codes = AccessCode.query.all()
    return ManyAccessCode.jsonify(all_codes)

