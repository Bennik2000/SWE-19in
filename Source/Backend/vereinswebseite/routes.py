from vereinswebseite import app, db
from flask import render_template


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/create_account')
def create_account():
    return render_template('create_account.jinja2')

@app.route('/account')
def personal_account_space():
    return render_template('personal_account_space.jinja2')