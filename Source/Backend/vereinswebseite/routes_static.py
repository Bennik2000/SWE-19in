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

    
@app.route('/static/style/reset_password.css')
def style_reset_password():
    return app.send_static_file('style/reset_password.css')

    
@app.route('/static/src/reset_password.js')
def src_reset_password():
    return app.send_static_file('src/reset_password.js')

@app.route('/static/src/FrontendHelper.js')
def src_FrontendHelper():
    return app.send_static_file('src/FrontendHelper.js')


# Set new password 
@app.route('/static/style/set_new_password.css')
def style_set_new_password():
    return app.send_static_file('style/set_new_password.css')

@app.route('/static/src/set_new_password.js')
def src_set_new_password():
    return app.send_static_file('src/set_new_password.js')
@app.route('/static/style/login.css')
def style_login():
    return app.send_static_file('style/login.css')

@app.route('/static/src/login.js')
def src_login():
    return app.send_static_file('src/login.js')

@app.route('/static/style/blog_post.css')
def style_blog_post():
    return app.send_static_file('style/create_and_edit_blog_post.css')

@app.route('/static/src/create_blog_post.js')
def src_create_blog_post():
    return app.send_static_file('src/create_blog_post.js')