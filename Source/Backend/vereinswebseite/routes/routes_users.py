from uuid import uuid4

from vereinswebseite.email_utils import send_reset_password_email
from vereinswebseite.models import db
from vereinswebseite.models.roles import Role
from vereinswebseite.models.token import AccessToken, PasswordResetToken
from vereinswebseite.models.user import UserSchema, User
from vereinswebseite.request_utils import success_response, generate_error
from vereinswebseite.decorators import roles_required
from flask import Blueprint, request, jsonify, abort, render_template, current_app
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from http import HTTPStatus

login_manager = LoginManager()

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
unauthorized_response = generate_error("Nicht authorisiert", HTTPStatus.UNAUTHORIZED)
user_id_invalid = generate_error("User ID ungültig", HTTPStatus.BAD_REQUEST)
roles_invalid = generate_error("Rolle(n) ungültig oder nicht gefunden", HTTPStatus.BAD_REQUEST)

users_bp = Blueprint('users', __name__, url_prefix='/api/users')
users_frontend_bp = Blueprint('users_frontend', __name__, url_prefix='/users')


@users_bp.route('', methods=['POST'])
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

    is_first_user = len(User.query.all()) == 0

    token = AccessToken.query.get(token_string)
    if token is None and not is_first_user and not current_app.debug:
        return token_invalid

    existing_user = User.query.filter_by(email=email).first()
    if existing_user is not None:
        return user_already_exists

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    if is_first_user:
        webmaster_role = Role.query.filter_by(name='Webmaster').first()
        new_user.roles = [webmaster_role, ]

    db.session.add(new_user)

    if not current_app.debug and token is not None:
        db.session.delete(token)

    db.session.commit()
    return success_response, 201


@users_bp.route('/login', methods=['POST', 'GET'])
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


@users_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return success_response


@users_bp.route('/personal_info', methods=['GET'])
@login_required
def personal_info():
    current_user_info = User.query.get(current_user.id)
    result = OneUser.jsonify(current_user_info)
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@users_bp.route('/change_password', methods=['POST'])
@login_required
def change_password():
    password = request.json.get("password")

    if password is None or password == "":
        return password_invalid

    current_user.set_password(password)
    db.session.commit()
    return success_response


@users_bp.route('/change_email', methods=['POST'])
@login_required
def change_email():
    email = request.json.get("email")

    if email is None or email == "":
        return email_invalid

    current_user.email = email
    db.session.commit()
    return success_response


@users_bp.route('', methods=['GET'])
@login_required
@roles_required('Webmaster')
def get_users():
    id_ = request.args.get("id", default="*")

    if id_ == "*":
        all_users = User.query.all()
        result = jsonify(ManyUsers.dump(all_users))
    else:
        user = User.query.get(id_)
        result = OneUser.jsonify(user)

    result.headers.add("Access-Control-Allow-Origin", "*")
    return result


@users_bp.route('/delete', methods=['DELETE'])
@login_required
def delete():
    db.session.delete(current_user)
    db.session.commit()
    logout_user()
    return success_response


@users_bp.route('/request_new_password', methods=['POST'])
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


@users_bp.route('/reset_password', methods=['POST'])
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


@users_bp.route('/current_user_roles', methods=['GET'])
@login_required
def current_user_roles():
    roles = [role.name for role in current_user.roles]

    return success_response | {
        "roles": roles
    }


@users_bp.route('/user_roles', methods=['GET'])
@login_required
@roles_required('Webmaster')
def get_user_roles():
    user_id = request.json.get("user_id")

    if user_id is None or user_id == "":
        return user_id_invalid

    user = User.query.get(user_id)
    if user is None:
        return user_id_invalid

    roles = [role.name for role in user.roles]

    return success_response | {
        "roles": roles
    }


@users_bp.route('/user_roles', methods=['PUT'])
@login_required
@roles_required('Webmaster')
def put_user_roles():
    user_id = request.json.get("user_id")
    role_names = request.json.get("roles")

    if user_id is None or user_id == "":
        return user_id_invalid

    if role_names is None:
        return roles_invalid

    roles = [Role.query.filter_by(name=role_name).first() for role_name in role_names]

    if None in roles:
        return roles_invalid

    user = User.query.get(user_id)
    if user is None:
        return user_id_invalid

    user.roles = roles

    return success_response


@users_frontend_bp.route('/reset_password/<reset_token>', methods=['GET'])
def reset_password_page(reset_token):
    token = PasswordResetToken.query.filter_by(token=reset_token).first()

    if token is None:
        return abort(HTTPStatus.NOT_FOUND)
    else:
        return render_template('set_new_password.jinja2', token=reset_token)


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    if request.path.startswith("/api/"):
        return unauthorized_response

    return render_template('unauthorized.jinja2'), HTTPStatus.UNAUTHORIZED
