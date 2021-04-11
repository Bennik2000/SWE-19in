from vereinswebseite import db, ma
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.UnicodeText)
    author_id = db.Column(db.String, db.ForeignKey('user.id'))

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    articles = db.relationship("Article")

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class AccessToken(db.Model):
    token = db.Column(db.String, primary_key=True)

    def __init__(self, token):
        self.token = token


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email')


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'author_id')


class AccessTokenSchema(ma.Schema):
    class Meta:
        fields = ('token', )
