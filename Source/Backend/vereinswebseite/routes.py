import json
from http import HTTPStatus

from vereinswebseite import app
from flask import render_template
from flask_login import login_required

from vereinswebseite.request_utils import success_response, generate_error

too_many_requests = generate_error("Too many requests", HTTPStatus.TOO_MANY_REQUESTS)
unauthorized = generate_error("Unauthorized", HTTPStatus.UNAUTHORIZED)


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/ping')
def ping_handler():
    return success_response


@app.route('/create_account')
def create_account():
    return render_template('create_account.jinja2')


@app.route('/login')
def render_login():
    return render_template('login.jinja2')


@app.route('/account')
@login_required
def personal_account_space():
    return render_template('personal_account_space.jinja2')

  
@app.errorhandler(HTTPStatus.TOO_MANY_REQUESTS)
def rate_limit_handler(e):
    response = e.get_response()
    response.data = json.dumps(too_many_requests[0])
    response.content_type = "application/json"
    return response


@app.errorhandler(HTTPStatus.UNAUTHORIZED)
def unauthorized_handler(e):
    response = e.get_response()
    response.data = json.dumps(unauthorized[0])
    response.content_type = "application/json"
    return response


@app.route('/reset_password')
def render_reset_password():
    return render_template('reset_password.jinja2')
