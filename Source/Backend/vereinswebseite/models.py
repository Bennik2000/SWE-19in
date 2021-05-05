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

    blog_posts = db.relationship("BlogPost")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


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
