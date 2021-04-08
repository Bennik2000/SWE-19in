from vereinswebseite import app, db, login_manager
from vereinswebseite.models import User, UserSchema, AccessToken
from vereinswebseite.errors import generate_error
from flask import request, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required
from http import HTTPStatus

# Init Schemas
OneUser = UserSchema()
ManyUsers = UserSchema(many=True)

# Errors
username_invalid = generate_error("User name invalid", HTTPStatus.BAD_REQUEST.value)
email_invalid = generate_error("Email invalid", HTTPStatus.BAD_REQUEST.value)
password_invalid = generate_error("Password invalid", HTTPStatus.BAD_REQUEST.value)
user_already_exists = generate_error("User already exists", HTTPStatus.CONFLICT.value)
already_authenticated = generate_error("Already authenticated", HTTPStatus.BAD_REQUEST.value)
email_or_password_wrong = generate_error("Email and/or password wrong", HTTPStatus.UNAUTHORIZED.value)
token_invalid = generate_error("Invalid access token", HTTPStatus.UNAUTHORIZED.value)


@app.route('/users', methods=['POST'])
def register_user():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')
    token_string = request.json.get('token')

    if name is None or name == "":
        return username_invalid

    if email is None or email == "":
        return email_invalid

    if password is None or password == "":
        return password_invalid

    #token = AccessToken.query.get(token_string)
    #if token is None:
        #return token_invalid

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return user_already_exists

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    # db.session.delete(token)
    db.session.commit()
    return {"success": True}, 201


@app.route('/users/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        abort(405)

    email = request.json.get('email')
    password = request.json.get('password')

    if email is None or email == "":
        return email_invalid

    if password is None or password == "":
        return password_invalid

    if current_user.is_authenticated:
        return already_authenticated

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password=password):
        return email_or_password_wrong

    login_user(user)
    return {"success": True}


@app.route("/users/logout")
@login_required
def logout():
    logout_user()
    return {"success": True}


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    abort(401)


@app.route('/users', methods=['GET'])
@login_required
def get_all_users():
    all_users = User.query.all()
    result = jsonify(ManyUsers.dump(all_users))
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@app.route('/users/<id>', methods=['GET'])
@login_required
def get_user(id_):
    user = User.query.get(id_)
    result = OneUser.jsonify(user)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result
