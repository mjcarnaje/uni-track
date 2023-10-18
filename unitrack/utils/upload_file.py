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

        if (os.path.exists(file_path)):
            print("File already exists")
            return filename

        file.save(file_path)

        print("File saved")

        return filename


def save_file_wtf(data: str or None) -> str or None:
    print("Saving file")
    if not data:
        print("No file part")
        return None

    data_filename = data.filename
    ext = data_filename.rsplit('.', 1)[1].lower()
    file_name = secure_filename(f"{uuid4()}.{ext}")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)

    if (os.path.exists(file_path)):
        print("File already exists")
        return file_name

    data.save(file_path)

    return file_name
