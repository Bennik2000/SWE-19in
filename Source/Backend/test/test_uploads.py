import os
import filecmp
import pathlib

import vereinswebseite
import flask_uploads
from http import HTTPStatus
from flask import Response
from werkzeug.datastructures import FileStorage
from test.base_test_case import BaseTestCase


class UploadsTest(BaseTestCase):
    # pathlib.Path(__file__).parent.absolute() gives us the directory where the current script is located.
    # We use this as a reference for relative file paths since vereinswebseite.app.root_path
    # depends on how the unit tests are started
    UPLOADS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "uploads")
    TEST_FILE_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "upload_test.jpeg")
    TEST_TEXT_FILE_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "upload_test.txt")

    def setUp(self) -> None:
        super().setUp(custom_config={
            "UPLOADED_IMAGES_DEST": self.UPLOADS_DIRECTORY
        })

    def test_given_logged_in_then_correct_return_value(self):
        self.create_and_login_test_user()
        response = self._send_upload_request()
        print(f"JSON response: {response.json}")

        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertTrue(success)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        os.remove(os.path.join(self.UPLOADS_DIRECTORY, response.json["filename"]))

    def test_given_logged_in_then_uploaded_correctly(self):
        self.create_and_login_test_user()
        response = self._send_upload_request()
        uploaded_file_path = os.path.join(self.UPLOADS_DIRECTORY, response.json["filename"])
        print(f"Uploaded file path: {uploaded_file_path}")

        uploaded_file_exists = os.path.isfile(uploaded_file_path)
        self.assertTrue(uploaded_file_exists, "The uploaded file doesn't exist in the upload directory")
        files_equal = filecmp.cmp(self.TEST_FILE_PATH, uploaded_file_path)
        self.assertTrue(files_equal, "The uploaded file isn't the same as the original file")
        os.remove(uploaded_file_path)

    def test_given_file_uploaded_then_served_correctly(self):
        self.create_and_login_test_user()
        upload_response = self._send_upload_request()
        filename = upload_response.json["filename"]

        download_response = self.app.get(f"/_uploads/images/{filename}")
        self.assertEqual(download_response.status_code, HTTPStatus.OK)
        # flask's helpers.send_file() doesn't close files automatically, so we have to do that manually:
        download_response.close()
        os.remove(os.path.join(self.UPLOADS_DIRECTORY, filename))

    def test_given_not_logged_in_then_not_uploaded(self):
        response = self._send_upload_request()

        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertFalse(success)

    def test_given_file_is_not_an_image_then_not_uploaded(self):
        self.create_and_login_test_user()
        test_file = FileStorage(stream=open(self.TEST_TEXT_FILE_PATH, "rb"))

        response = self.app.post(
            "/api/upload_image",
            data={"image": test_file},
            content_type='multipart/form-data'
        )

        print(f"JSON response: {response.json}")
        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertFalse(success)

    def test_given_no_files_in_request_then_success_false(self):
        self.create_and_login_test_user()
        response = self.app.post("/api/upload_image", content_type='multipart/form-data')

        print(f"JSON response: {response.json}")
        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertFalse(success)

    def _send_upload_request(self) -> Response:
        test_file = FileStorage(stream=open(self.TEST_FILE_PATH, "rb"))

        response = self.app.post(
            "/api/upload_image",
            data={"image": test_file},
            content_type='multipart/form-data'
        )

        return response

