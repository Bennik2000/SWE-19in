# Originally copied from
# https://github.com/lingthio/Flask-User/blob/5c652e6479036c3d33aa1626524e4e65bd3b961e/flask_user/decorators.py
from functools import wraps
from flask import current_app, g
from flask_login import current_user


def roles_accepted(*role_names):
    """| This decorator ensures that the current user is logged in,
    | and has *at least one* of the specified roles (OR operation).
    Example::
        @route('/edit_article')
        @roles_accepted('Writer', 'Editor')
        def edit_article():  # User must be 'Writer' OR 'Editor'
            ...
    """
    # convert the list to a list containing that list.
    # Because roles_required(a, b) requires A AND B
    # while roles_required([a, b]) requires A OR B
    def wrapper(func):

        @wraps(func)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            # User must have the required roles
            # NB: roles_required would call has_roles(*role_names): ('A', 'B') --> ('A', 'B')
            # But: roles_accepted must call has_roles(role_names):  ('A', 'B') --< (('A', 'B'),)
            if not current_user.has_roles(role_names):
                return current_app.login_manager.unauthorized()

            # It's OK to call the view
            return func(*args, **kwargs)

        return decorator

    return wrapper


def roles_required(*role_names):
    """| This decorator ensures that the current user is logged in,
    | and has *all* of the specified roles (AND operation).
    Example::
        @route('/escape')
        @roles_required('Special', 'Agent')
        def escape_capture():  # User must be 'Special' AND 'Agent'
            ...
    """
    def wrapper(func):
        @wraps(func)    # Tells debuggers that is is a function wrapper
        def decorator(*args, **kwargs):
            if not current_user.has_roles(*role_names):
                # Redirect to the unauthorized page
                return current_app.login_manager.unauthorized()
            # It's OK to call the view
            return func(*args, **kwargs)
        return decorator
    return wrapper
