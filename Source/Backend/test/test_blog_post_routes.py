from http import HTTPStatus
from base_test_case import BaseTestCase
from vereinswebseite.models import db, BlogPost


class BlogPostRoutesTest(BaseTestCase):
    POST_TITLE = "Original blog post title"
    POST_CONTENT = "Original blog post content"

    def test_given_blog_posts_exists_when_edit_then_no_error(self):
        test_user = self.create_and_login_test_user()

        blog_post = BlogPost(self.POST_TITLE, self.POST_CONTENT, test_user.id)
        db.session.add(blog_post)
        db.session.commit()

        response = self.app.get("/blog_posts/edit?post_id=" + str(blog_post.id))

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_given_blog_posts_does_not_exist_when_edit_then_error(self):
        self.create_and_login_test_user()
        response = self.app.get("/blog_posts/edit?post_id=1")

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_given_not_logged_in_when_edit_then_error(self):
        response = self.app.get("/blog_posts/edit?post_id=1")

        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)
