from flask import Flask
from flask_uploads import configure_uploads
from vereinswebseite import config


def create_app(test_config=None):
    app = Flask('vereinswebseite',
                static_url_path='')

    # Allow adding a route '' to a blueprint with a url prefix
    app.url_map.strict_slashes = False
    app.config.from_pyfile('config.py')
    if test_config is not None:
        app.config.from_mapping(test_config)

    from vereinswebseite.models import db
    from vereinswebseite.routes.routes_users import login_manager
    from vereinswebseite.email_utils import mail
    from vereinswebseite.routes.routes_uploads import images
    from vereinswebseite.routes import limiter, ma
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    configure_uploads(app, images)
    limiter.init_app(app)
    ma.init_app(app)

    from vereinswebseite.routes import general_bp
    from vereinswebseite.routes.routes_accss_token import access_token_bp
    from vereinswebseite.routes.routes_blog_posts import blog_posts_bp, blog_posts_frontend_bp
    from vereinswebseite.routes.routes_static import static_bp
    from vereinswebseite.routes.routes_uploads import uploads_bp
    from vereinswebseite.routes.routes_users import users_bp, users_frontend_bp
    app.register_blueprint(general_bp)
    app.register_blueprint(access_token_bp)
    app.register_blueprint(blog_posts_bp)
    app.register_blueprint(blog_posts_frontend_bp)
    app.register_blueprint(static_bp)
    app.register_blueprint(uploads_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(users_frontend_bp)

    return app


def init_db():
    from vereinswebseite.models import db
    from vereinswebseite.models.roles import Role

    db.create_all()

    for role_name in config.ROLES:
        if Role.query.filter_by(name=role_name).first() is None:
            db.session.add(Role(name=role_name))

    db.session.commit()
