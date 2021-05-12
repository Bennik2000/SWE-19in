from datetime import datetime
from http import HTTPStatus

import markdown
from flask_login import login_required, current_user

from vereinswebseite.models.blog_post import BlogPostSchema, BlogPost, RenderedPost
from vereinswebseite.models.user import User
from vereinswebseite.routes import limiter
from vereinswebseite.models import db
from flask import request, abort, render_template, Blueprint

from vereinswebseite.request_utils import get_int_from_request, success_response, generate_error, generate_success, \
    parse_date

OneBlogPost = BlogPostSchema()
ManyBlogPost = BlogPostSchema(many=True)

title_invalid = generate_error("Titel ungültig", HTTPStatus.BAD_REQUEST)
content_invalid = generate_error("Inhalt ungültig", HTTPStatus.BAD_REQUEST)
user_invalid = generate_error("Benutzer ID ungültig", HTTPStatus.BAD_REQUEST)
blog_post_id_invalid = generate_error("Blog Post ID ungültig", HTTPStatus.BAD_REQUEST)
date_format_invalid = generate_error("Falsches Datumsformat.", HTTPStatus.BAD_REQUEST)
not_permitted_to_edit_or_delete = generate_error("Dieser Post gehört zu einem anderen Benutzer. "
                                                 "Daher kann er nicht bearbeitet oder gelöscht werden.",
                                                 HTTPStatus.FORBIDDEN)

blog_posts_bp = Blueprint('blog_posts', __name__, url_prefix='/api/blog_posts')
blog_posts_frontend_bp = Blueprint('blog_posts_frontend', __name__, url_prefix='/blog_posts')


@blog_posts_bp.route('', methods=['POST'])
@login_required
def add_blog_post():
    title = request.json.get('title')
    content = request.json.get('content')
    expiration_date_string = request.json.get('expiration_date')

    if title is None or title == "":
        return title_invalid

    if content is None or content == "":
        return content_invalid

    if current_user is None:
        return user_invalid

    success, expiration_date = parse_date(expiration_date_string)

    if not success:
        return date_format_invalid

    new_article = BlogPost(title, content, current_user.id, datetime.now(), expiration_date)

    db.session.add(new_article)
    db.session.commit()
    return success_response


@blog_posts_bp.route('/update', methods=['PUT'])
@login_required
def update_blog_post():
    id_ = request.json.get('id')
    title = request.json.get('title')
    content = request.json.get('content')
    expiration_date_string = request.json.get('expiration_date')

    if id_ is None or title == "":
        return blog_post_id_invalid

    if title is None or title == "":
        return title_invalid

    if content is None or content == "":
        return content_invalid

    success, expiration_date = parse_date(expiration_date_string)
    if not success:
        return date_format_invalid

    post = BlogPost.query.get(id_)
    if post is None:
        return blog_post_id_invalid

    if post.author_id != current_user.id:
        return not_permitted_to_edit_or_delete

    post.expiration_date = expiration_date
    post.title = title
    post.content = content
    db.session.commit()

    return success_response


@blog_posts_bp.route('', methods=['GET'])
def get_all_blog_posts():
    posts = BlogPost.query.all()
    all_posts = []
    for post in posts:
        if post.is_expired():
            continue

        user = User.query.get(post.author_id)

        post_obj = {
            "id": post.id,
            "title": post.title,
            "content": post.make_post_summary(),
            "creation_date": post.creation_date,
            "expiration_date": post.expiration_date,
            "author": user.name,
            "author_id": post.author_id
        }
        all_posts.append(post_obj)

    return generate_success({
        "blog_posts": all_posts
    })


@blog_posts_bp.route('/delete', methods=['DELETE'])
@login_required
def delete_blog_post():
    post_id = request.json.get("id")

    post = BlogPost.query.get(post_id)

    if post.author_id != current_user.id:
        return not_permitted_to_edit_or_delete

    db.session.delete(post)
    db.session.commit()

    return success_response


@blog_posts_bp.route('/render_preview', methods=['POST'])
@limiter.limit("5 per second")
def render_blog_post_preview():
    content = request.json.get("content")

    if content is None:
        return content_invalid

    html = markdown.markdown(content, extensions=["extra"])

    return generate_success({
        "html": html
    })


@blog_posts_frontend_bp.route('/all', methods=['GET'])
def render_all_blog_posts():
    posts = BlogPost.query.all()
    all_posts = []

    for post in posts:
        if post.is_expired():
            continue

        user = User.query.get(post.author_id)
        username = ""

        if user is not None:
            username = user.name


        can_edit = False

        if current_user.id == post.author_id:
            can_edit = True
        
        all_posts.append(RenderedPost(

            post_id=post.id,
            title=post.title,
            summary=markdown.markdown(post.make_post_summary()),
            content=None,
            creation_date=post.creation_date,
            name=username,
            can_edit_post=can_edit
        ))
        
    return render_template('all_blog_posts.jinja2', posts=all_posts)


@blog_posts_frontend_bp.route('/create')
@login_required
def render_create_blog_post():
    return render_template('create_blog_post.jinja2')


@blog_posts_frontend_bp.route('/edit', methods=['GET'])
@login_required
def render_edit_blog_post():
    post_id = get_int_from_request("post_id")
    post = BlogPost.query.get(post_id)

    if post is None:
        abort(HTTPStatus.NOT_FOUND)

    return render_template('edit_blog_post.jinja2',
                           title=post.title,
                           content=post.content,
                           creation_date=post.creation_date,
                           expiration_date=post.expiration_date,
                           id=post.id)


@blog_posts_frontend_bp.route('/render', methods=['GET'])
def render_blog_post():
    post_id = get_int_from_request("post_id")
    post = BlogPost.query.get(post_id)

    if post is None:
        abort(HTTPStatus.NOT_FOUND)

    if post.is_expired():
        abort(HTTPStatus.NOT_FOUND)

    html = markdown.markdown(post.content, extensions=["extra"])

    author = User.query.get(post.author_id)
    author_name = ""

    if author is not None:
        author_name = author.name

    can_edit = current_user.is_authenticated
    can_delete = current_user.is_authenticated

    return render_template("whole_blog_post.jinja2",
                           can_edit_post=can_edit,
                           can_delete_post=can_delete,
                           post=html,
                           title=post.title,
                           author=author_name, 
                           id=post_id,
                           date=post.creation_date)
