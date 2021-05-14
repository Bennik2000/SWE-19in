from . import db

from vereinswebseite.routes import ma


class PasswordResetToken(db.Model):
    token = db.Column(db.String, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __init__(self, token, user):
        self.token = token
        self.user = user


class AccessToken(db.Model):
    token = db.Column(db.String, primary_key=True)

    def __init__(self, token):
        self.token = token


class AccessTokenSchema(ma.Schema):
    class Meta:
        fields = ('token',)
