from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from ..models.Course import Course

course_bp = Blueprint('course', __name__)


@course_bp.route('/<int:id>', methods=['DELETE'])
@login_required
def course(id):
    Course.delete(university_id=current_user.id, id=id)
    return jsonify({'success': True})


@course_bp.route('/college/<int:college_id>')
@login_required
def courses(college_id):
    courses = Course.find_by_college_id(
        university_id=current_user.id, college_id=college_id)
    return jsonify(courses)
