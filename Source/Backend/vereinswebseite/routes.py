from vereinswebseite import app, db
from flask import render_template


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/create_account')
def create_account():
    return render_template('create_account.jinja2')


@app.route('/set_new_password')
def set_new_password():
    return render_template('set_new_password.jinja2')