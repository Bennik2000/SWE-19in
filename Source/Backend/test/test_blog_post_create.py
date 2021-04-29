import unittest

from test.test_utils import setup_test_app, create_and_login_test_user
from vereinswebseite.models import BlogPost


class BlogPostTest(unittest.TestCase):
    POST_TITLE = "Title of post"
    POST_CONTENT = "This sentence is written 100 times to create a long blog post. " * 100

    def setUp(self) -> None:
        self.app = setup_test_app()

    def test_given_not_logged_in_when_create_blog_post_then_created_in_db(self):
        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
            "content": self.POST_CONTENT,
        })

        self.assertFalse(response.json["success"])

    def test_given_correct_request_when_create_blog_post_then_created_in_db(self):
        create_and_login_test_user(self.app)

        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
            "content": self.POST_CONTENT,
        })

        self.assertTrue(response.json["success"])

        posts = BlogPost.query.all()

        self.assertEqual(len(posts), 1)
        self.assertEqual(posts[0].title, self.POST_TITLE)
        self.assertEqual(posts[0].content, self.POST_CONTENT)

    def test_given_title_missing_when_create_blog_post_then_error(self):
        create_and_login_test_user(self.app)

        response = self.app.post("/api/blog_posts", json={
            "content": self.POST_CONTENT,
        })

        self.assertFalse(response.json["success"])

    def test_given_content_missing_when_create_blog_post_then_error(self):
        create_and_login_test_user(self.app)

        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
        })

        self.assertFalse(response.json["success"])
