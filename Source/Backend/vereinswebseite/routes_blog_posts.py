from http import HTTPStatus

from flask_login import login_required, current_user

from vereinswebseite import app, db
from vereinswebseite.errors import generate_error
from vereinswebseite.models import BlogPost, BlogPostSchema, User
from flask import request, jsonify

OneBlogPost = BlogPostSchema()
ManyBlogPost = BlogPostSchema(many=True)

title_invalid = generate_error("Titel ungültig", HTTPStatus.BAD_REQUEST.value)
content_invalid = generate_error("Inhalt ungültig", HTTPStatus.BAD_REQUEST.value)
user_invalid = generate_error("Benutzer Id ungültig", HTTPStatus.BAD_REQUEST.value)


@app.route('/blog_posts', methods=['POST'])
@login_required
def add_blog_post():
    title = request.json.get('title')
    content = request.json.get('content')

    if title is None or title == "":
        return title_invalid

    if content is None or content == "":
        return content_invalid

    if current_user is None:
        return user_invalid

    new_article = BlogPost(title, content, current_user.id)

    db.session.add(new_article)
    db.session.commit()
    return {"success": True}


@app.route('/blog_posts', methods=['GET'])
def get_all_blog_posts():
    posts = BlogPost.query.all()

    all_posts = []

    for post in posts:
        user = User.query.get(post.author_id)

        post_obj = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": user.name,
            "author_id": post.author_id
        }
        all_posts.append(post_obj)

    return jsonify({"success": True, "blog_posts": all_posts})
