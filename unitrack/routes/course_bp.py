from flask import Blueprint, url_for, redirect, request, jsonify
from flask_login import current_user, login_required

from ..models.Course import Course
from ..utils.upload_file import save_file_wtf, save_file
from ..validations import AddCourseValidation, UpdateCourseValidation

course_bp = Blueprint('course', __name__)


@course_bp.route('/add', methods=['POST'])
@login_required
def add_course():
    form = AddCourseValidation()

    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            code=form.code.data,
            photo=save_file_wtf(data=form.photo.data),
            college_id=form.college_id.data,
            university_id=current_user.id
        )

        course.insert()

        return redirect(url_for('college.college', id=course.college_id))

    return jsonify(form.errors)


@course_bp.route('/<int:id>', methods=['POST', 'GET', 'DELETE'])
@login_required
def course(id):
    course_query = Course(id=id)

    if request.method == "POST":
        updated_course = Course(
            id=id,
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=save_file(key='photo'),
            college_id=request.form.get('college_id'),
            university_id=current_user.id
        )

        updated_course.update()

        return redirect(f'/college/{updated_course.college_id}')

    if request.method == "DELETE":
        course_query.delete()

        return jsonify({'success': True})

    return jsonify(course_query.find_one())


@course_bp.route('/college/<int:id>', methods=['GET'])
@login_required
def courses_by_college(id):
    courses_by_college = Course(
        university_id=current_user.id).find_by_college_id(college_id=id)
    return jsonify(courses_by_college)
