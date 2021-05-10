import json
from http import HTTPStatus

from vereinswebseite.request_utils import success_response, generate_error
from flask import render_template, Blueprint
from flask_login import login_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_marshmallow import Marshmallow

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "60 per hour"]
)
ma = Marshmallow()

too_many_requests = generate_error("Too many requests", HTTPStatus.TOO_MANY_REQUESTS)
unauthorized = generate_error("Unauthorized", HTTPStatus.UNAUTHORIZED)

general_bp = Blueprint('general', __name__)


@general_bp.route('/')
def index():
    return render_template('index.jinja2')


@general_bp.route('/ping')
def ping_handler():
    return success_response


@general_bp.route('/create_account')
def create_account():
    return render_template('create_account.jinja2')


@general_bp.route('/login')
def render_login():
    return render_template('login.jinja2')


@general_bp.route('/account')
@login_required
def personal_account_space():
    return render_template('personal_account_space.jinja2')

  
@general_bp.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
def rate_limit_handler(e):
    response = e.get_response()
    response.data = json.dumps(too_many_requests[0])
    response.content_type = "application/json"
    return response


@general_bp.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized_handler(e):
    response = e.get_response()
    response.data = json.dumps(unauthorized[0])
    response.content_type = "application/json"
    return response


@general_bp.route('/reset_password')
def render_reset_password():
    return render_template('reset_password.jinja2')

@app.route('/navigation_page')
def render_navigation_page():
    return render_template('navigation_page.jinja2')



