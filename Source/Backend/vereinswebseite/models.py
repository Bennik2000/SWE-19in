from datetime import datetime

from vereinswebseite import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)

    def __init__(self, title, content, author_id, creation_date=datetime.now(), expiration_date=None):
        self.title = title
        self.content = content
        self.author_id = author_id
        self.creation_date = creation_date
        self.expiration_date = expiration_date

    def __repr__(self):
        return f'BlogPost(id={self.id}, author_id={self.author_id},\n' \
               f'\ttitle="{self.title}",\n\tcontent="{self.content}")'

    def make_post_summary(self):
        summary_length_in_words = 100

        words = self.content.split(' ')

        if len(words) > summary_length_in_words:
            return ' '.join(words[0:summary_length_in_words]) + "..."
        return self.content

    def is_expired(self):
        if self.expiration_date is None:
            return False

        return self.expiration_date.date() < datetime.today().date()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

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


class AccessToken(db.Model):
    token = db.Column(db.String, primary_key=True)

    def __init__(self, token):
        self.token = token


class PasswordResetToken(db.Model):
    token = db.Column(db.String, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __init__(self, token, user):
        self.token = token
        self.user = user


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)


class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'author_id', 'creation_date', 'expiration_date')


class AccessTokenSchema(ma.Schema):
    class Meta:
        fields = ('token',)
