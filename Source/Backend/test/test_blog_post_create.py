from base_test_case import BaseTestCase
from vereinswebseite.models import BlogPost


class BlogPostTest(BaseTestCase):
    POST_TITLE = "Title of post"
    POST_CONTENT = "This sentence is written 100 times to create a long blog post. " * 100

    def test_given_not_logged_in_when_create_blog_post_then_created_in_db(self):
        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
            "content": self.POST_CONTENT,
        })

        self.assertFalse(response.json["success"])

    def test_given_correct_request_when_create_blog_post_then_created_in_db(self):
        self.create_and_login_test_user()

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
        self.create_and_login_test_user()

        response = self.app.post("/api/blog_posts", json={
            "content": self.POST_CONTENT,
        })

        self.assertFalse(response.json["success"])

    def test_given_content_missing_when_create_blog_post_then_error(self):
        self.create_and_login_test_user()

        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
        })

        self.assertFalse(response.json["success"])

    def test_given_correct_expiration_date_when_create_blog_post_then_no_error(self):
        self.create_and_login_test_user()

        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
            "content": self.POST_CONTENT,
            "expiration_date": "2021-04-30"
        })

        self.assertTrue(response.json["success"])

    def test_given_wrong_expiration_date_when_create_blog_post_then_error(self):
        self.create_and_login_test_user()

        response = self.app.post("/api/blog_posts", json={
            "title": self.POST_TITLE,
            "content": self.POST_CONTENT,
            "expiration_date": "202.04.30"
        })

        self.assertFalse(response.json["success"])
