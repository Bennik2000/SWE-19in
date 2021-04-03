from unittest import TestCase
from vereinswebseite import app, db

from vereinswebseite.models import AccessToken


class AccessTokenRoutesTest(TestCase):
    AccessTokenToDelete = "AccessTokenToDelete"

    def setUp(self) -> None:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    def test_given_no_access_tokens_when_create_access_token_then_correct_created(self):
        response = self.app.post("/accessToken")
        print(f"JSON response: {response.json}")
        self.assertTrue(len(response.json["token"]) == 8)

    def test_given_access_token_existing_when_delete_access_token_then_correct_deleted(self):
        db.session.add(AccessToken(self.AccessTokenToDelete))
        db.session.commit()

        response = self.app.get(f"/accessToken/delete", json={"token": self.AccessTokenToDelete})

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["deleted"])
        self.assertIsNone(AccessToken.query.get(self.AccessTokenToDelete))

    def test_given_access_token_not_existing_when_delete_access_token_then_error(self):
        response = self.app.get(f"/accessToken/delete", json={"token": "tokenThatDoesNotExist"})

        print(f"JSON response: {response.json}")
        self.assertIsNotNone(response.status_code, 404)
        self.assertIsNotNone(response.json["errors"])
        self.assertFalse(response.json["deleted"])

    def test_given_access_token_exists_when_validate_then_access_token_valid(self):
        db.session.add(AccessToken("ExistingAccessToken"))
        db.session.commit()

        response = self.app.get(f"/accessToken/validate", json={"token": "ExistingAccessToken"})

        print(f"JSON response: {response.json}")
        self.assertTrue(response.json["valid"])

    def test_given_access_token_does_not_exist_when_validate_then_access_token_invalid(self):
        response = self.app.get(f"/accessToken/validate", json={"token": "NotExistingAccessToken"})

        print(f"JSON response: {response.json}")
        self.assertFalse(response.json["valid"])

    def test_given_some_access_tokens_when_get_all_then_all_returned(self):
        db.session.add(AccessToken("token1"))
        db.session.add(AccessToken("token2"))
        db.session.commit()

        response = self.app.get(f"/accessToken")

        print(f"JSON response: {response.json}")
        self.assertTrue(len(response.json["tokens"]) >= 2)
