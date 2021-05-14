from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from vereinswebseite.routes import ma


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_picture = db.Column(db.String, nullable=True, unique=True)

    roles = db.relationship('Role', secondary='user_roles')
    blog_posts = db.relationship("BlogPost")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    # Originally copied from
    # https://github.com/lingthio/Flask-User/blob/5c652e6479036c3d33aa1626524e4e65bd3b961e/flask_user/user_mixin.py
    def has_roles(self, *requirements):
        """ Return True if the user has all of the specified roles. Return False otherwise.
            has_roles() accepts a list of requirements:
                has_role(requirement1, requirement2, requirement3).
            Each requirement is either a role_name, or a tuple_of_role_names.
                role_name example:   'manager'
                tuple_of_role_names: ('funny', 'witty', 'hilarious')
            A role_name-requirement is accepted when the user has this role.
            A tuple_of_role_names-requirement is accepted when the user has ONE of these roles.
            has_roles() returns true if ALL of the requirements have been accepted.
            For example:
                has_roles('a', ('b', 'c'), 'd')
            Translates to:
                User has role 'a' AND (role 'b' OR role 'c') AND role 'd'"""

        role_names = [role.name for role in self.roles]

        # has_role() accepts a list of requirements
        for requirement in requirements:
            if isinstance(requirement, (list, tuple)):
                # this is a tuple_of_role_names requirement
                tuple_of_role_names = requirement
                authorized = False
                for role_name in tuple_of_role_names:
                    if role_name in role_names:
                        # tuple_of_role_names requirement was met: break out of loop
                        authorized = True
                        break
                if not authorized:
                    return False  # tuple_of_role_names requirement failed: return False
            else:
                # this is a role_name requirement
                role_name = requirement
                # the user must have this role
                if role_name not in role_names:
                    return False  # role_name requirement failed: return False

        # All requirements have been met: return True
        return True


class NamedRelation(ma.Field):
    def __init__(self, name_column, **kwargs):
        super().__init__(**kwargs)
        self.name_column = name_column

    def serialize(self, attr, obj, accessor=None):
        return [getattr(related, self.name_column) for related in getattr(obj, attr)]


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        include_relationships = True

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    roles = NamedRelation(name_column="name")
