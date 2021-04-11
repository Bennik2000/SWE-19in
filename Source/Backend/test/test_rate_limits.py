from unittest import TestCase

from test.test_utils import setup_test_app
from vereinswebseite import app, db


class RateLimitTest(TestCase):

    def setUp(self) -> None:
        self.app = setup_test_app(limiter_enabled=True)

    def test_rate_limit(self):
        did_exceed_rate_limit = False

        for i in range(1, 100):
            response = self.app.get("/ping")

            if not response.json["success"]:
                if response.json["errors"][0]["status"] == "429":
                    did_exceed_rate_limit = True

        self.assertTrue(did_exceed_rate_limit)
