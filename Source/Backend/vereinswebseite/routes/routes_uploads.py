import uuid
import os.path
from http import HTTPStatus

from vereinswebseite.request_utils import generate_error, generate_success
from flask_login import login_required
from flask import request, Blueprint
from flask_uploads import UploadSet, IMAGES, UploadNotAllowed


images = UploadSet('images', IMAGES)

wrong_file_type = generate_error("Dieser Dateityp kann nicht hochgeladen werden. "
                                 "Nur Bilder sind erlaubt.", HTTPStatus.BAD_REQUEST)
no_image_given = generate_error("Keine Bilddatei im Request vorhanden", HTTPStatus.BAD_REQUEST)

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/api/upload_image', methods=['POST'])
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
        return generate_success({
            "filename": filename
        }, status=HTTPStatus.CREATED)
    except UploadNotAllowed:
        return wrong_file_type
