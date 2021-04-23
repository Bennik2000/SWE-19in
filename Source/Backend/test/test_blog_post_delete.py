import unittest

from test.test_utils import setup_test_app, create_and_login_test_user, add_test_user
from vereinswebseite import db
from vereinswebseite.models import BlogPost


class DeleteBlogPostTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = setup_test_app()

    def test_given_correct_request_when_delete_blog_post_then_deleted_in_db(self):
        create_and_login_test_user(self.app)
        db.session.add(BlogPost("Title", "Content", 1))
        db.session.commit()

        response = self.app.delete("/blog_posts/delete", json={
            "id": "1",
        })

        self.assertTrue(response.json["success"])

        posts = BlogPost.query.all()
        self.assertEqual(len(posts), 0)

    def test_given_not_own_post_when_delete_blog_post_then_error(self):
        create_and_login_test_user(self.app)
        db.session.add(BlogPost("Title1", "Content1", 2))
        db.session.commit()

        response = self.app.delete("/blog_posts/delete", json={
            "id": "1",
        })

        self.assertFalse(response.json["success"])

        posts = BlogPost.query.all()
        self.assertEqual(len(posts), 1)

    def test_given_not_logged_in_post_when_delete_blog_post_then_error(self):
        add_test_user()
        db.session.add(BlogPost("Title", "Content", 1))
        db.session.commit()

        response = self.app.delete("/blog_posts/delete", json={
            "id": "1",
        })

        self.assertFalse(response.json["success"])

        posts = BlogPost.query.all()
        self.assertEqual(len(posts), 1)