import unittest
from http import HTTPStatus

import flask

from test.test_utils import setup_test_app, add_test_user, create_and_login_test_user, TestPassword
from vereinswebseite.models import BlogPost, User
from vereinswebseite import db


class BlogPostRoutesTest(unittest.TestCase):
    POST_TITLE = "Original blog post title"
    POST_CONTENT = "Original blog post content"

    def setUp(self) -> None:
        self.app = setup_test_app()

    def test_given_blog_posts_exists_when_edit_then_no_error(self):
        test_user = create_and_login_test_user(self.app)

        blog_post = BlogPost(self.POST_TITLE, self.POST_CONTENT, test_user.id)
        db.session.add(blog_post)
        db.session.commit()

        response = self.app.get("/blog_posts/edit/" + str(blog_post.id))

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_given_blog_posts_does_not_exist_when_edit_then_error(self):
        create_and_login_test_user(self.app)
        response = self.app.get("/blog_posts/edit/1")

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_given_not_logged_in_when_edit_then_error(self):
        response = self.app.get("/blog_posts/edit/1")

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
