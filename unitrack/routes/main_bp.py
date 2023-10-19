from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required

from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student
from ..models.University import University

from ..utils.upload_file import save_file

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    if current_user and current_user.is_authenticated:
        student_count = Student(university_id=current_user.id).count()
        college_count = College(university_id=current_user.id).count()
        course_count = Course(university_id=current_user.id).count()
        return render_template("dashboard.html",
                               student_count=student_count,
                               college_count=college_count,
                               course_count=course_count)
    return render_template("home.html")


@main_bp.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    university = University(id=current_user.id).find_by_id()

    if (request.method == "POST"):
        university.email = request.form.get("email")
        university.name = request.form.get("name")
        university.display_name = request.form.get("display_name")
        university.primary_color = request.form.get("primary_color")
        university.secondary_color = request.form.get("secondary_color")
        university.logo = save_file(key='logo') or university.logo

        university.update()

        return redirect("/settings")

    return render_template("settings.html", university=university)
