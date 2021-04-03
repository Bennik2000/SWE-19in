from vereinswebseite import app


@app.route('/static/style/main.css')
def style():
    return app.send_static_file('main.css')

@app.route('/static/style/create_account.css')
def styleCreateAccount():
    return app.send_static_file('style/create_account.css')

    
@app.route('/static/src/create_account.js')
def srcCreateAccount():
    return app.send_static_file('src/create_account.js')