import os
from werkzeug.exceptions import RequestEntityTooLarge
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.utils import cloudinary_url
from flask import (Blueprint, jsonify, redirect, render_template, request,
                   send_from_directory)
from flask_login import current_user, login_required

from unitrack.config import Config

from ..db.seed import seed
from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student
from ..models.University import University
from ..utils.upload_file import upload_file
from ..validations import UpdateUniversityValidation

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    if current_user and current_user.is_authenticated:
        student_count = Student.count(university_id=current_user.id)
        college_count = College.count(university_id=current_user.id)
        course_count = Course.count(university_id=current_user.id)
        return render_template("dashboard.html",
                               student_count=student_count,
                               college_count=college_count,
                               course_count=course_count)
    return render_template("home.html")


@main_bp.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    form = UpdateUniversityValidation()
    university = University.find_by_id(id=current_user.id)

    if form.validate_on_submit():
        University.update(id=current_user.id, email=form.email.data, logo=form.logo.data, name=form.name.data,
                          display_name=form.display_name.data, primary_color=form.primary_color.data, secondary_color=form.secondary_color.data)

        return redirect("/settings")

    form.id.data = university.id
    form.email.data = university.email
    form.name.data = university.name
    form.display_name.data = university.display_name
    form.primary_color.data = university.primary_color
    form.secondary_color.data = university.secondary_color
    form.logo.data = university.logo

    return render_template("settings.html", form=form, university=university)


@main_bp.route('/upload', methods=['POST'])
def upload_to_dir():
    return jsonify({'url': upload_file('upload')})


@main_bp.route('/upload/<path:filename>')
def get_image_dir(filename):
    pathlike = filename or 'default.png'
    return send_from_directory(Config.UPLOAD_FOLDER, pathlike, as_attachment=True)


@main_bp.route('/upload/cloudinary', methods=['POST'])
def upload_to_cloudinary():
    file = request.files.get('upload')

    if not file:
        return jsonify({
            'is_success': False,
            'error': 'Missing file'
        })

    size = len(file.read())
    file.seek(0)

    one_mb = 1000 * 1000

    if size > one_mb:
        return jsonify({
            'is_success': False,
            'error': 'File too large'
        }), 413

    if file:
        upload_result = cloudinary_upload(
            file, folder=Config.CLOUDINARY_FOLDER)

        return jsonify({
            'is_success': True,
            'public_id': upload_result['public_id'],
            'url': upload_result['secure_url']
        })

    return jsonify({
        'is_success': False,
        'error': 'Missing file'
    })


@main_bp.route('/seed', methods=['POST', 'GET'])
def seed_database():
    if request.method == 'POST':
        seed()
        return redirect('/')
    return render_template('seed_database.html')
