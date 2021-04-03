from vereinswebseite import app, db, login_manager
from vereinswebseite.models import User, UserSchema
from flask import request, jsonify, abort, render_template
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
        return {
            "errors": [
                {
                    "title": "User already exists",
                    "status": "409",
                }
            ],
            "user_registered": False
        }, 409

    new_user = User(name=name, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return {"user_registered": True}, 201


@app.route('/users/login', methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        abort(405)

    email = request.json['email']
    password = request.json['password']

    if current_user.is_authenticated:
        return {
            "errors": [
                {
                    "title": "Already authenticated",
                    "status": "400",
                }
            ],
            "logged_in": False
        }, 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password=password):
        return {
            "errors": [
                {
                    "title": "Email and/or password wrong",
                    "status": "400",
                }
            ],
            "logged_in": False
        }, 400

    login_user(user)
    return {"logged_in": True}


@app.route("/users/logout")
@login_required
def logout():
    logout_user()
    return {"logged_out": True}


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
