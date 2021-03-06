from datetime import datetime
from http import HTTPStatus

from test.base_test_case import BaseTestCase, TestUserName
from vereinswebseite.models import db
from vereinswebseite.models.blog_post import BlogPost


class GetBlogPostsTest(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.add_test_user()

    def test_given_not_logged_in_when_get_all_then_all_returned(self):
        db.session.add(BlogPost("Title", "Content", 1))
        db.session.add(BlogPost("Title1", "Content1", 1))
        db.session.add(BlogPost("Title", "Content", 1, expiration_date=datetime(2020, 2, 1)))
        db.session.commit()
        response = self.app.get("/api/blog_posts")

        self.assertTrue(response.json["success"])
        self.assertEqual(len(response.json["blog_posts"]), 2)
        self.assertEqual(response.json["blog_posts"][0]["title"], "Title")
        self.assertEqual(response.json["blog_posts"][0]["content"], "Content")
        self.assertEqual(response.json["blog_posts"][0]["author"], TestUserName)
        self.assertEqual(response.json["blog_posts"][0]["author_id"], 1)
        self.assertEqual(response.json["blog_posts"][0]["id"], 1)
        self.assertEqual(response.json["blog_posts"][1]["id"], 2)

    def test_normal_blog_post_when_render_blog_post_then_no_error(self):
        db.session.add(BlogPost("Title", "Content", 1, expiration_date=datetime(2030, 2, 1)))
        db.session.commit()
        response = self.app.get("/blog_posts/render?post_id=1")

        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_expired_blog_post_when_render_blog_post_then_error(self):
        db.session.add(BlogPost("Title", "Content", 1, expiration_date=datetime(2020, 2, 1)))
        db.session.commit()
        response = self.app.get("/blog_posts/render?post_id=1")

        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_not_expired_blog_post_when_render_blog_post_then_no_error_dates_same_day(self):
        db.session.add(BlogPost("Title", "Content", 1, expiration_date=datetime.today()))
        db.session.commit()
        response = self.app.get("/blog_posts/render?post_id=1")

        self.assertEqual(response.status_code, HTTPStatus.OK)
