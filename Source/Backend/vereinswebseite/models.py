from vereinswebseite import db, ma


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    author_id = db.Column(db.String, db.ForeignKey('user.id'))

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    articles = db.relationship("Article")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'password')


class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'author_id')
