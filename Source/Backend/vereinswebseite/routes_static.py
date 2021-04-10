from vereinswebseite import app


@app.route('/static/style/main.css')
def style():
    return app.send_static_file('main.css')

@app.route('/static/style/create_account.css')
def style_create_account():
    return app.send_static_file('style/create_account.css')

@app.route('/static/src/create_account.js')
def src_create_account():
    return app.send_static_file('src/create_account.js')

    
@app.route('/static/style/reset_password.css')
def style_reset_password():
    return app.send_static_file('style/reset_password.css')