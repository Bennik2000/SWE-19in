import uuid
import os.path
from http import HTTPStatus


from vereinswebseite import app, images
from vereinswebseite.errors import generate_error
from flask_login import login_required
from flask import request
import flask_uploads

wrong_file_type = generate_error("Dieser Dateityp kann nicht hochgeladen werden. "
                                 "Nur Bilder sind erlaubt.", HTTPStatus.BAD_REQUEST)
no_image_given = generate_error("Keine Bilddatei im Request vorhanden", HTTPStatus.BAD_REQUEST)


@app.route('/upload_image', methods=['POST'])
@login_required
def upload_image():
    if 'image' not in request.files:
        return no_image_given

    image = request.files['image']
    file_extension = os.path.splitext(image.filename)[1]
    random_filename = str(uuid.uuid4())[:8] + file_extension
    image.filename = random_filename

    try:
        filename = images.save(image)
        return {
            "success": True,
            "filename": filename
        }, HTTPStatus.CREATED
    except flask_uploads.UploadNotAllowed:
        return wrong_file_type
