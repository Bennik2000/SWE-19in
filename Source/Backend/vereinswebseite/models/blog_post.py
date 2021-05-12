from datetime import datetime

from vereinswebseite.routes import ma

from . import db


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


class RenderedPost:
    def __init__(self, post_id, title, summary, content, creation_date, name,can_edit_post):
        self.id = post_id
        self.title = title
        self.summary = summary
        self.content = content
        self.creation_date = creation_date
        self.name = name
        self.edit = can_edit_post


class BlogPostSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'content', 'author_id', 'creation_date', 'expiration_date')
