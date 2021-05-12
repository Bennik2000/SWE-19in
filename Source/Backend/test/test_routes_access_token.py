from test.base_test_case import BaseTestCase
from vereinswebseite.models import db
from vereinswebseite.models.token import AccessToken
from vereinswebseite.routes.routes_accss_token import AccessTokenLength


class AccessTokenRoutesTest(BaseTestCase):
    AccessTokenToDelete = "AccessTokenToDelete"

    def test_given_no_access_tokens_when_create_access_token_then_correct_created(self):
        response = self.app.post("/api/accessToken")
        print(f"JSON response: {response.json}")
        self.assertEqual(len(response.json["token"]), AccessTokenLength)

    def test_given_access_token_existing_when_delete_access_token_then_correct_deleted(self):
        db.session.add(AccessToken(self.AccessTokenToDelete))
        db.session.commit()

        response = self.app.get(f"/api/accessToken/delete", json={"token": self.AccessTokenToDelete})

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["success"])
        self.assertIsNone(AccessToken.query.get(self.AccessTokenToDelete))

    def test_given_access_token_not_existing_when_delete_access_token_then_error(self):
        response = self.app.get(f"/api/accessToken/delete", json={"token": "tokenThatDoesNotExist"})

        print(f"JSON response: {response.json}")
        self.assertIsNotNone(response.status_code, 404)
        self.assertIsNotNone(response.json["errors"])
        self.assertFalse(response.json["success"])

    def test_given_access_token_exists_when_validate_then_access_token_valid(self):
        db.session.add(AccessToken("ExistingAccessToken"))
        db.session.commit()

        response = self.app.get(f"/api/accessToken/validate", json={"token": "ExistingAccessToken"})

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["valid"])

    def test_given_access_token_does_not_exist_when_validate_then_access_token_invalid(self):
        response = self.app.get(f"/api/accessToken/validate", json={"token": "NotExistingAccessToken"})

        print(f"JSON response: {response.json}")
        self.assertFalse(response.json["valid"])

    def test_given_some_access_tokens_when_get_all_then_all_returned(self):
        db.session.add(AccessToken("token1"))
        db.session.add(AccessToken("token2"))
        db.session.commit()

        response = self.app.get(f"/api/accessToken")

        print(f"JSON response: {response.json}")
        self.assertTrue(len(response.json["tokens"]) >= 2)
