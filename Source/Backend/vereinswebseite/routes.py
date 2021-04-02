from vereinswebseite import app, db
from flask import render_template


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/create-account')
def createAccount():
    return render_template('create_account.jinja2')
