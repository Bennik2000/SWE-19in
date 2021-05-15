from flask import Blueprint, current_app

static_bp = Blueprint('static', __name__, url_prefix='/static')


# Main
@static_bp.route('/style/main.css')
def style():
    return current_app.send_static_file('main.css')


# Create new account
@static_bp.route('/style/create_account.css')
def style_create_account():
    return current_app.send_static_file('style/create_account.css')


@static_bp.route('/style/personal_account_space.css')
def style_personal_account_space():
    return current_app.send_static_file('style/personal_account_space.css')

    
@static_bp.route('/src/personal_account_space.js')
def src_personal_account_space():
    return current_app.send_static_file('src/personal_account_space.js')


@static_bp.route('/src/create_account.js')
def src_create_account():
    return current_app.send_static_file('src/create_account.js')

    
@static_bp.route('/style/reset_password.css')
def style_reset_password():
    return current_app.send_static_file('style/reset_password.css')

    
@static_bp.route('/src/reset_password.js')
def src_reset_password():
    return current_app.send_static_file('src/reset_password.js')


@static_bp.route('/src/FrontendHelper.js')
def src_frontend_helper():
    return current_app.send_static_file('src/FrontendHelper.js')


# Set new password 
@static_bp.route('/style/set_new_password.css')
def style_set_new_password():
    return current_app.send_static_file('style/set_new_password.css')


@static_bp.route('/src/set_new_password.js')
def src_set_new_password():
    return current_app.send_static_file('src/set_new_password.js')


@static_bp.route('/style/unauthorized.css')
def style_unauthorized():
    return current_app.send_static_file('style/login.css')


@static_bp.route('/style/login.css')
def style_login():
    return current_app.send_static_file('style/login.css')


@static_bp.route('/src/login.js')
def src_login():
    return current_app.send_static_file('src/login.js')


@static_bp.route('/style/create_and_edit_blog_post.css')
def style_blog_post():
    return current_app.send_static_file('style/create_and_edit_blog_post.css')


@static_bp.route('/src/create_and_edit_blog_post.js')
def src_create_blog_post():
    return current_app.send_static_file('src/create_and_edit_blog_post.js')


@static_bp.route('/style/whole_blog_post.css')
def style_whole_blog_post():
    return current_app.send_static_file('style/whole_blog_post.css')

  
@static_bp.route('/src/edit_blog_post.js')
def src_edit_blog_post():
    return current_app.send_static_file('src/edit_blog_post.js')

  
@static_bp.route('/style/navigation_page.css')
def style_navigation_page():
    return current_app.send_static_file('style/navigation_page.css')


@static_bp.route('/src/whole_blog_post.js')
def src_whole_blog_post():
    return current_app.send_static_file('src/whole_blog_post.js')

@static_bp.route('style/all_blog_posts.css')
def style_blog_overview():
    return current_app.send_static_file('style/all_blog_posts.css')

@static_bp.route('/src/all_blog_posts.js')
def src_blog_overview():
    return current_app.send_static_file('src/all_blog_posts.js')