from flask import Blueprint, render_template
from flask_login import current_user

from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    if current_user.is_authenticated:
        student_count = Student(university_id=current_user.id).count()
        college_count = College(university_id=current_user.id).count()
        course_count = Course(university_id=current_user.id).count()
        return render_template("dashboard.html",
                               student_count=student_count,
                               college_count=college_count,
                               course_count=course_count)
    return render_template("home.html")
