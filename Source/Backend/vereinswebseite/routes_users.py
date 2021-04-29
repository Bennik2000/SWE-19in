from uuid import uuid4

from vereinswebseite import app, db, login_manager
from vereinswebseite.email_utils import send_reset_password_email
from vereinswebseite.models import User, UserSchema, AccessToken, PasswordResetToken
from vereinswebseite.errors import generate_error
from flask import request, jsonify, abort, render_template
from flask_login import current_user, login_user, logout_user, login_required
from http import HTTPStatus

# Init Schemas
OneUser = UserSchema()
ManyUsers = UserSchema(many=True)

# Errors
username_invalid = generate_error("Name ungültig", HTTPStatus.BAD_REQUEST)
email_invalid = generate_error("Email ungültig", HTTPStatus.BAD_REQUEST)
password_invalid = generate_error("Passwort ungültig", HTTPStatus.BAD_REQUEST)
user_already_exists = generate_error("Account existiert bereits", HTTPStatus.CONFLICT)
already_authenticated = generate_error("Bereits eingeloggt", HTTPStatus.BAD_REQUEST)
email_or_password_wrong = generate_error("Email und/oder Passwort falsch", HTTPStatus.UNAUTHORIZED)
token_invalid = generate_error("Registrierungscode ungültig", HTTPStatus.UNAUTHORIZED)
reset_token_invalid = generate_error("Code ungültig", HTTPStatus.UNAUTHORIZED)


success_response = {"success": True}


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

    token = AccessToken.query.get(token_string)
    if token is None and not app.debug:
        return token_invalid

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return user_already_exists

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)

    if not app.debug:
        db.session.delete(token)

    db.session.commit()
    return success_response, 201


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
    return success_response


@app.route("/users/logout")
@login_required
def logout():
    logout_user()
    return success_response


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    return {"success": False}, HTTPStatus.UNAUTHORIZED


@app.route('/users/personal_info', methods=['GET'])
@login_required
def personal_info():
    current_user_info = User.query.get(current_user.id)
    result = OneUser.jsonify(current_user_info)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@app.route('/users/change_password', methods=['POST'])
@login_required
def change_password():
    password = request.json.get("password")

    if password is None or password == "":
        return password_invalid

    current_user.set_password(password)
    db.session.commit()
    return success_response

@app.route('/users/change_email', methods = ['POST'])
@login_required
def change_email():
    email = request.json.get("email")

    if email is None or email == "":
        return email_invalid

    current_user.email = email
    db.session.commit()
    return success_response



@app.route('/users', methods=['GET'])
@login_required
# TODO: Webmaster role required
def get_users():
    id_ = request.args.get("id", default="*")

    result = None

    if id_ == "*":
        all_users = User.query.all()
        result = jsonify(ManyUsers.dump(all_users))
    else:
        user = User.query.get(id_)
        result = OneUser.jsonify(user)

    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@app.route('/users/delete', methods=['DELETE'])
@login_required
def delete():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return success_response


@app.route('/users/request_new_password', methods=['POST'])
def request_new_password():
    email = request.json.get('email')

    if email is None or email == "":
        return email_invalid

    user = User.query.filter_by(email=email).first()

    if not user:
        return success_response

    token_string = str(uuid4()).upper() + str(uuid4()).upper()
    token = PasswordResetToken(token_string, user)

    db.session.add(token)
    db.session.commit()

    link = request.url_root + "users/reset_password/" + token_string
    send_reset_password_email(user, link)

    return success_response


@app.route('/users/reset_password/<reset_token>', methods=['GET'])
def reset_password_page(reset_token):
    token = PasswordResetToken.query.filter_by(token=reset_token).first()

    if token is None:
        return abort(HTTPStatus.NOT_FOUND)
    else:
        return render_template('set_new_password.jinja2', token=reset_token)


@app.route('/users/reset_password', methods=['POST'])
def reset_password():
    password = request.json.get("password")
    reset_token = request.json.get("token")

    if password is None or password == "":
        return password_invalid

    token = PasswordResetToken.query.filter_by(token=reset_token).first()

    if token is None:
        return reset_token_invalid

    token.user.set_password(password)
    db.session.delete(token)
    db.session.commit()

    return success_response
