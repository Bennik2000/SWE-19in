from vereinswebseite import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.UnicodeText)
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id

    def __repr__(self):
        return f'BlogPost(id={self.id}, author_id={self.author_id},\n' \
               f'\ttitle="{self.title}",\n\tcontent="{self.content}")'


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


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'author_id')


class AccessTokenSchema(ma.Schema):
    class Meta:
        fields = ('token', )
