from flask import Blueprint, jsonify, redirect, request
from flask_login import login_required

from ..models.Course import Course
from ..utils.upload_file import save_file

course_bp = Blueprint('course', __name__)


@course_bp.route('/', methods=['POST'])
@login_required
def courses():
    if request.method == "POST":
        course = Course(
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=save_file(key='photo'),
            college_id=request.form.get('college_id')
        )

        course.insert()

        return redirect(f'/college/{course.college_id}')


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
            college_id=request.form.get('college_id')
        )

        updated_course.update()

        return redirect(f'/college/{updated_course.college_id}')

    if request.method == "DELETE":
        course_query.delete()

        return jsonify({'success': True})

    return jsonify(course_query.find_one())


@course_bp.route('/college/<int:id>', methods=['GET'])
def courses_by_college(id):
    courses_by_college = Course().find_by_college_id(college_id=id)
    return jsonify(courses_by_college)
