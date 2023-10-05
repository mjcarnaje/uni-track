import os
from flask import request, current_app as app
from werkzeug.utils import secure_filename
from uuid import uuid4

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_file(key: str, file_name: str or None = None) -> str or None:
    file = request.files.get(key)

    if not file:
        print("No file part")
        return None

    if file.filename == '':
        print("No selected file")
        return None

    if allowed_file(file.filename):
        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        filename = f"{file_name or uuid4()}.{ext}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print("File saved")
        return filename
