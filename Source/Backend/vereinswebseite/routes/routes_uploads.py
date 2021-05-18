import uuid
import os.path
from http import HTTPStatus

from vereinswebseite.models import db
from vereinswebseite.request_utils import generate_error, generate_success
from flask_login import login_required, current_user
from flask import request, Blueprint
from flask_uploads import UploadSet, IMAGES, UploadNotAllowed

images = UploadSet('images', IMAGES)

wrong_file_type = generate_error("Dieser Dateityp kann nicht hochgeladen werden. "
                                 "Nur Bilder sind erlaubt.", HTTPStatus.BAD_REQUEST)
no_image_given = generate_error("Keine Bilddatei im Request vorhanden", HTTPStatus.BAD_REQUEST)

uploads_bp = Blueprint('uploads', __name__)


@uploads_bp.route('/api/upload_image', methods=['POST'])
@login_required
def api_upload_image():
    success, response, filename = _save_uploaded_file()
    return response


@uploads_bp.route('/api/upload_profile_picture', methods=['POST'])
@login_required
def api_upload_profile_picture():
    success, response, filename = _save_uploaded_file()

    if success:
        current_user.profile_picture = filename
        db.session.commit()

    return response


def _save_uploaded_file():
    if 'image' not in request.files:
        return False, no_image_given, None

    image = request.files['image']
    file_extension = os.path.splitext(image.filename)[1]
    random_filename = str(uuid.uuid4())[:8] + file_extension
    image.filename = random_filename

    try:
        filename = images.save(image)
        return True, generate_success({
            "filename": filename
        }, status=HTTPStatus.CREATED), filename
    except UploadNotAllowed:
        return False, wrong_file_type, None
