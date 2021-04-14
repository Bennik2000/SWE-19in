from vereinswebseite import app

# Main
@app.route('/static/style/main.css')
def style():
    return app.send_static_file('main.css')


# Create new account
@app.route('/static/style/create_account.css')
def style_create_account():
    return app.send_static_file('style/create_account.css')

@app.route('/static/src/create_account.js')
def src_create_account():
    return app.send_static_file('src/create_account.js')

    

# Set new password 
@app.route('/static/style/set_new_password.css')
def style_set_new_password():
    return app.send_static_file('style/set_new_password.css')

@app.route('/static/src/set_new_password.js')
def src_set_new_password():
    return app.send_static_file('src/set_new_password.js')