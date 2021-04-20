import unittest

from test.test_utils import setup_test_app, add_test_user
from vereinswebseite import db
from vereinswebseite.models import BlogPost


class GetAllBlogPostsTest(unittest.TestCase):

    def setUp(self) -> None:
        self.app = setup_test_app()
        add_test_user()

    def test_given_not_logged_in_when_create_blog_post_then_created_in_db(self):
        db.session.add(BlogPost("Title", "Content", 1))
        db.session.add(BlogPost("Title1", "Content1", 1))
        response = self.app.get("/blog_post")

        self.assertTrue(response.json["success"])
        self.assertEqual(len(response.json["blog_posts"]), 2)
        self.assertEqual(response.json["blog_posts"][0]["title"], "Title")
        self.assertEqual(response.json["blog_posts"][0]["content"], "Content")
