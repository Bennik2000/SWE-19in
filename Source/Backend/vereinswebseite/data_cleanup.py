import os
import re

from flask import current_app
from flask_uploads import IMAGES

from vereinswebseite.models.blog_post import BlogPost
from vereinswebseite.post_rendering import post_renderer
from vereinswebseite.routes.routes_uploads import images


def delete_unused_images():
    """
    This function deletes all unused images from the file system. This prevents trashing the
    file system with not used images and thus saves storage
    """
    posts = BlogPost.query.all()

    all_used_images = []

    for post in posts:
        all_used_images.extend(post_renderer.get_all_images(post.content))

    all_images = _get_all_uploaded_image_filenames()

    obsolete_images = set(all_images) ^ set(all_used_images)

    for image_name in obsolete_images:
        _delete_image(image_name)


def _delete_image(image_name):
    try:
        fn = images.path(image_name)
        if os.path.isfile(fn):
            os.remove(fn)
    except:
        pass


def _get_all_uploaded_image_filenames():
    image_dir = current_app.config["UPLOADED_IMAGES_DEST"]
    try:
        filenames = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
        filenames = [f for f in filenames if f.endswith(IMAGES)]
        return filenames
    except FileNotFoundError:
        return []
