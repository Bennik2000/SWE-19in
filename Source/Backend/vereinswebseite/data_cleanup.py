import os
import re

from flask import current_app
from flask_uploads import IMAGES

from vereinswebseite.models.blog_post import BlogPost
from vereinswebseite.routes.routes_uploads import images


def delete_unused_images():
    posts = BlogPost.query.all()

    all_used_images = []

    for post in posts:
        all_used_images.extend(_get_images_in_post(post))

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


def _get_images_in_post(post):
    # This regex matches all images in a markdown document
    all_image_urls = re.findall(r'!\[.*?]\(([^ ]+).*?\)', post.content)
    all_image_names = []

    for url in all_image_urls:

        # This regex extracts the image name from an image url
        name = re.findall(r'.*/([a-zA-Z0-9]+\.[a-zA-Z0-9]+)', url)

        if len(name) == 1:
            all_image_names.append(name[0])

    return all_image_names
