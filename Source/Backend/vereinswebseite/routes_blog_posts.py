from http import HTTPStatus

import markdown
from flask_login import login_required, current_user

from vereinswebseite import app, db
from vereinswebseite.models import BlogPost, BlogPostSchema, User
from flask import request, abort, render_template

from vereinswebseite.request_utils import get_int_from_request, success_response, generate_error, generate_success

OneBlogPost = BlogPostSchema()
ManyBlogPost = BlogPostSchema(many=True)

title_invalid = generate_error("Titel ungültig", HTTPStatus.BAD_REQUEST)
content_invalid = generate_error("Inhalt ungültig", HTTPStatus.BAD_REQUEST)
user_invalid = generate_error("Benutzer ID ungültig", HTTPStatus.BAD_REQUEST)
blog_post_id_invalid = generate_error("Blog Post ID ungültig", HTTPStatus.BAD_REQUEST)
not_permitted_to_edit_or_delete = generate_error("Dieser Post gehört zu einem anderen Benutzer. "
                                                 "Daher kann er nicht bearbeitet oder gelöscht werden.",
                                                 HTTPStatus.FORBIDDEN)


@app.route('/api/blog_posts', methods=['POST'])
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
    return success_response


@app.route('/api/blog_posts/update', methods=['PUT'])
@login_required
def update_blog_post():
    id_ = request.json.get('id')
    title = request.json.get('title')
    content = request.json.get('content')

    if id_ is None or title == "":
        return blog_post_id_invalid

    if title is None or title == "":
        return title_invalid

    if content is None or content == "":
        return content_invalid

    post = BlogPost.query.get(id_)
    if post is None:
        return blog_post_id_invalid

    if post.author_id != current_user.id:
        return not_permitted_to_edit_or_delete

    post.title = title
    post.content = content
    db.session.commit()

    return success_response


@app.route('/api/blog_posts', methods=['GET'])
def get_all_blog_posts():
    posts = BlogPost.query.all()

    all_posts = []

    for post in posts:
#        user = User.query.get(post.author_id)

        post_obj = {
            "id": post.id,
            "title": post.title,
            "content": post.make_post_summary(),
            "author": "user.name",
            "author_id": post.author_id
        }
        all_posts.append(post_obj)

    return generate_success({
        "blog_posts": all_posts
    })


@app.route('/api/blog_posts/delete', methods=['DELETE'])
@login_required
def delete_blog_post():
    post_id = request.json.get("id")

    post = BlogPost.query.get(post_id)

    if post.author_id != current_user.id:
        return not_permitted_to_edit_or_delete

    db.session.delete(post)
    db.session.commit()

    return success_response


@app.route('/blog_posts/create')
def render_create_blog_post():
    return render_template('create_blog_post.jinja2')


@app.route('/blog_posts/edit', methods=['GET'])
@login_required
def render_edit_blog_post():
    post_id = get_int_from_request("post_id")
    post = BlogPost.query.get(post_id)

    if post is None:
        abort(HTTPStatus.NOT_FOUND)

    return render_template('edit_blog_post.jinja2',
                           title=post.title,
                           content=post.content,
                           id=post.id)


@app.route('/blog_posts/render', methods=['GET'])
def render_blog_post():
    post_id = get_int_from_request("post_id")
    post = BlogPost.query.get(post_id)

    if post is None:
        abort(HTTPStatus.NOT_FOUND)

    html = markdown.markdown(post.content)

    author = User.query.get(post.author_id)
    author_name = ""

    if author is not None:
        author_name = author.name

    return render_template("blog_post.jinja2", post=html, title=post.title, author=author_name)


@app.route('/api/blog_posts/render_preview', methods=['POST'])
def render_blog_post_preview():
    content = request.json.get("content")

    if content is None:
        return content_invalid

    html = markdown.markdown(content)

    return generate_success({
        "html": html
    })
