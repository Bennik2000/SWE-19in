from vereinswebseite import app


@app.route('/static/style/main.css')
def style():
    return app.send_static_file('main.css')

@app.route('/static/style/create_account.css')
def style_create_account():
    return app.send_static_file('style/create_account.css')

@app.route('/static/style/personal_account_space.css')
def style_personal_account_space():
    return app.send_static_file('style/personal_account_space.css')
    

@app.route('/static/src/create_account.js')
def src_create_account():
    return app.send_static_file('src/create_account.js')
    
@app.route('/static/src/personal_account_space.js')
def src_personal_account_space():
    return app.send_static_file('src/personal_account_space.js')