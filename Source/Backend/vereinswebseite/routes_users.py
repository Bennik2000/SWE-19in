from vereinswebseite import app, db, login_manager
from vereinswebseite.models import User, UserSchema
from flask import request, jsonify, abort
from flask_login import current_user, login_user, logout_user, login_required

# Init Schemas
OneUser = UserSchema()
ManyUsers = UserSchema(many=True)


@app.route('/users', methods=['POST'])
def register_user():
    name = request.json['name']
    email = request.json['email']
    password = request.json['password']

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return "User already exists", 409

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return "User registered", 201


@app.route('/users/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        abort(400)

    email = request.json['email']
    password = request.json['password']

    if current_user.is_authenticated:
        return "Already authenticated"

    user = User.query.filter_by(email=email).first()

    if not user:
        return "User not found", 404

    if user.check_password(password=password):
        login_user(user)
        return "Login successful"

    return "Wrong password", 403


@app.route("/users/logout")
@login_required
def logout():
    logout_user()
    return "Logged out"


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return "Error: unauthorized", 401


@app.route('/users', methods=['GET'])
def get_all_users():
    all_users = User.query.all()
    result = jsonify(ManyUsers.dump(all_users))
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    result = OneUser.jsonify(user)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result
