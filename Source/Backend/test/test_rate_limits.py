from http import HTTPStatus

from base_test_case import BaseTestCase


class RateLimitTest(BaseTestCase):
    def setUp(self) -> None:
        super().setUp(limiter_enabled=True)

    def test_rate_limit(self):
        did_exceed_rate_limit = False

        for i in range(1, 100):
            response = self.app.get("/ping")

            if not response.json["success"]:
                if response.json["errors"][0]["status"] == HTTPStatus.TOO_MANY_REQUESTS:
                    did_exceed_rate_limit = True

        self.assertTrue(did_exceed_rate_limit)
