import unittest
import flask

from test.test_utils import setup_test_app, add_test_user, create_and_login_test_user, TestPassword
from vereinswebseite.models import BlogPost, User
from vereinswebseite import db


class BlogPostTest(unittest.TestCase):
    ORIGINAL_POST_TITLE = "Original blog post title"
    ORIGINAL_POST_CONTENT = "Original blog post content"
    NEW_POST_TITLE = "New blog post title"
    NEW_POST_CONTENT = "New blog post content"

    def setUp(self) -> None:
        self.app = setup_test_app()

    def test_given_correct_user_logged_in_then_updated_correctly(self):
        test_user = create_and_login_test_user(self.app)
        blog_post_id = self._add_original_blog_post(test_user.id)
        response = self._send_update_request(blog_post_id)

        success = response.json.get("success")
        self.assertIsNotNone(success)
        self.assertTrue(success)

        blog_post = BlogPost.query.get(blog_post_id)
        self.assertEqual(blog_post.title, self.NEW_POST_TITLE)
        self.assertEqual(blog_post.content, self.NEW_POST_CONTENT)

    def test_given_not_logged_in_then_not_updated(self):
        test_user = add_test_user()
        blog_post_id = self._add_original_blog_post(test_user.id)
        response = self._send_update_request(blog_post_id)

        success = response.json.get("success")
        self.assertIsNotNone(success)
        self.assertFalse(success, "Got success=True, even though we are not logged in")
        self._assert_blog_post_not_updated(blog_post_id)

    def test_given_wrong_user_logged_in_then_not_updated(self):
        test_user = add_test_user()
        blog_post_id = self._add_original_blog_post(test_user.id)
        self._add_and_login_second_testuser()
        response = self._send_update_request(blog_post_id)

        print(f"JSON response: {response.json}")
        success = response.json.get("success")
        self.assertIsNotNone(success)
        self.assertFalse(success, "Got success=True, even though the wrong user is logged in")
        self._assert_blog_post_not_updated(blog_post_id)

    def _add_original_blog_post(self, user_id) -> int:
        blog_post = BlogPost(self.ORIGINAL_POST_TITLE, self.ORIGINAL_POST_CONTENT, user_id)
        db.session.add(blog_post)
        db.session.commit()
        
        return blog_post.id

    def _send_update_request(self, blog_post_id) -> flask.Response:
        response = self.app.put("/api/blog_posts/update", json={
            "id": blog_post_id,
            "title": self.NEW_POST_TITLE,
            "content": self.NEW_POST_CONTENT,
        })

        return response

    def _assert_blog_post_not_updated(self, blog_post_id):
        blog_post = BlogPost.query.get(blog_post_id)

        self.assertEqual(blog_post.title, self.ORIGINAL_POST_TITLE,
                         "Blog post title was updated, even though this was not allowed.")
        self.assertEqual(blog_post.content, self.ORIGINAL_POST_CONTENT,
                         "Blog post content was updated, even though this was not allowed.")

    def _add_and_login_second_testuser(self) -> User:
        email = "test2@email.com"
        test_user2 = User(name="TestUser2", email=email)
        test_user2.set_password(TestPassword)
        db.session.add(test_user2)
        db.session.commit()

        self.app.post("/users/login", json={
            "email": email,
            "password": TestPassword
        })

        return test_user2
