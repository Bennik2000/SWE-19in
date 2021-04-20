from http import HTTPStatus

from flask_login import login_required

from vereinswebseite import app, db
from vereinswebseite.errors import generate_error
from vereinswebseite.models import BlogPost, BlogPostSchema, User
from flask import request, jsonify

OneBlogPost = BlogPostSchema()
ManyBlogPost = BlogPostSchema(many=True)

title_invalid = generate_error("Titel ungültig", HTTPStatus.BAD_REQUEST.value)
content_invalid = generate_error("Inhalt ungültig", HTTPStatus.BAD_REQUEST.value)
user_invalid = generate_error("Benutzer Id ungültig", HTTPStatus.BAD_REQUEST.value)


@app.route('/blog_post', methods=['POST'])
@login_required
def add_blog_post():
    title = request.json.get('title')
    content = request.json.get('content')
    author_user_id = request.json.get('author_user_id')

    if title is None or title == "":
        return title_invalid

    if content is None or content == "":
        return content_invalid

    user = User.query.get(author_user_id)
    if user is None:
        return user_invalid

    new_article = BlogPost(title, content, author_user_id)

    db.session.add(new_article)
    db.session.commit()
    return {"success": True}


@app.route('/blog_post', methods=['GET'])
def get_all_blog_posts():
    all_articles = BlogPost.query.all()
    result = jsonify({"success": True, "blog_posts": ManyBlogPost.dump(all_articles)})
    result.headers.add("Access-Control-Allow-Origin", "*")
    return result
