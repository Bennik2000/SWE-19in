import os
import pathlib

from werkzeug.datastructures import FileStorage

from test.base_test_case import BaseTestCase


class DeleteBlogPostImagesTest(BaseTestCase):
    UPLOADS_DIRECTORY = os.path.join(pathlib.Path(__file__).parent.absolute(), "..", "uploads")
    TEST_FILE_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "upload_test.jpeg")

    def setUp(self) -> None:
        super().setUp(custom_config={
            "UPLOADED_IMAGES_DEST": self.UPLOADS_DIRECTORY
        })

    def test_on_delete_post_images_are_deleted(self):
        self.create_and_login_test_user()
        uploaded_file_path = self._create_blog_post_with_image()

        self._delete_blog_post()

        uploaded_file_exists = os.path.isfile(uploaded_file_path)
        self.assertFalse(uploaded_file_exists, "The uploaded file was not deleted")

    def test_on_update_post_images_are_deleted(self):
        self.create_and_login_test_user()
        uploaded_file_path = self._create_blog_post_with_image()

        uploaded_file_path_new, path_new = self._send_upload_request()

        self._edit_blog_post("#Title\n![Alt-text](/_uploads/images/" + uploaded_file_path_new + "){: style='width: 5vw;'}")

        uploaded_file_exists = os.path.isfile(path_new)
        self.assertTrue(uploaded_file_exists, "The uploaded file was deleted")

        uploaded_file_exists = os.path.isfile(uploaded_file_path)
        self.assertFalse(uploaded_file_exists, "The uploaded file was not deleted")

    def _create_blog_post_with_image(self):
        image_filename, path = self._send_upload_request()
        self._create_blog_post("#Title\n![Alt-text](/_uploads/images/" + image_filename + "){: style='width: 5vw;'}")

        uploaded_file_exists = os.path.isfile(path)
        self.assertTrue(uploaded_file_exists, "The uploaded file doesn't exist in the upload directory")
        return image_filename

    def _delete_blog_post(self):
        self.app.delete("/api/blog_posts/delete", json={
            "id": "1",
        })

    def _create_blog_post(self, content):
        self.app.post("/api/blog_posts", json={
            "title": "Title",
            "content": content,
        })

    def _edit_blog_post(self, new_content):
        self.app.put("/api/blog_posts/update", json={
            "id": "1",
            "title": "Title",
            "content": new_content,
        })

    def _send_upload_request(self) -> (str, str):
        test_file = FileStorage(stream=open(self.TEST_FILE_PATH, "rb"))

        response = self.app.post(
            "/api/upload_image",
            data={"image": test_file},
            content_type='multipart/form-data'
        )

        filename = response.json["filename"]

        return filename, os.path.join(self.UPLOADS_DIRECTORY, filename)
