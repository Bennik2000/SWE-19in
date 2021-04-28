import os
import unittest
import filecmp

import vereinswebseite
import flask_uploads
from http import HTTPStatus
from flask import Response
from werkzeug.datastructures import FileStorage
from test.test_utils import setup_test_app, create_and_login_test_user


class UploadsTest(unittest.TestCase):
    # The root_path is Backend/test when a test is run. So we have to adjust it here.
    UPLOADS_DIRECTORY = os.path.join(vereinswebseite.app.root_path, "..", "uploads")
    TEST_FILE_PATH = os.path.join(vereinswebseite.app.root_path, "upload_test.jpeg")
    TEST_TEXT_FILE_PATH = os.path.join(vereinswebseite.app.root_path, "upload_test.txt")

    def setUp(self) -> None:
        vereinswebseite.app.config['UPLOADED_IMAGES_DEST'] = self.UPLOADS_DIRECTORY
        flask_uploads.configure_uploads(vereinswebseite.app, vereinswebseite.images)
        self.app = setup_test_app()

    def test_given_logged_in_then_correct_return_value(self):
        create_and_login_test_user(self.app)
        response = self._send_upload_request()
        print(f"JSON response: {response.json}")

        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertTrue(success)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        os.remove(os.path.join(self.UPLOADS_DIRECTORY, response.json["filename"]))

    def test_given_logged_in_then_uploaded_correctly(self):
        create_and_login_test_user(self.app)
        response = self._send_upload_request()
        uploaded_file_path = os.path.join(self.UPLOADS_DIRECTORY, response.json["filename"])
        print(f"Uploaded file path: {uploaded_file_path}")

        uploaded_file_exists = os.path.isfile(uploaded_file_path)
        self.assertTrue(uploaded_file_exists, "The uploaded file doesn't exist in the upload directory")
        files_equal = filecmp.cmp(self.TEST_FILE_PATH, uploaded_file_path)
        self.assertTrue(files_equal, "The uploaded file isn't the same as the original file")
        os.remove(uploaded_file_path)

    def test_given_file_uploaded_then_served_correctly(self):
        create_and_login_test_user(self.app)
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
        create_and_login_test_user(self.app)
        test_file = FileStorage(stream=open(self.TEST_TEXT_FILE_PATH, "rb"))

        response = self.app.post(
            "/upload_image",
            data={"image": test_file},
            content_type='multipart/form-data'
        )

        print(f"JSON response: {response.json}")
        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertFalse(success)

    def test_given_no_files_in_request_then_success_false(self):
        create_and_login_test_user(self.app)
        response = self.app.post("/upload_image", content_type='multipart/form-data')

        print(f"JSON response: {response.json}")
        success = response.json["success"]
        self.assertIsNotNone(success)
        self.assertFalse(success)

    def _send_upload_request(self) -> Response:
        test_file = FileStorage(stream=open(self.TEST_FILE_PATH, "rb"))

        response = self.app.post(
            "/upload_image",
            data={"image": test_file},
            content_type='multipart/form-data'
        )

        return response

