from flask import Blueprint, render_template, request, redirect
from flask_login import current_user, login_required

from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student
from ..models.University import University

from ..utils.upload_file import save_file_wtf
from ..validations import UpdateUniversityValidation

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
    form = UpdateUniversityValidation()
    university = University(id=current_user.id).find_by_id()

    if form.validate_on_submit():
        university.email = form.email.data
        university.name = form.name.data
        university.display_name = form.display_name.data
        university.primary_color = form.primary_color.data
        university.secondary_color = form.secondary_color.data
        university.logo = save_file_wtf(
            data=form.logo.data, default_filename=university.logo)

        university.update()

        return redirect("/settings")

    form.id.data = university.id
    form.email.data = university.email
    form.name.data = university.name
    form.display_name.data = university.display_name
    form.primary_color.data = university.primary_color
    form.secondary_color.data = university.secondary_color
    form.logo.data = university.logo

    return render_template("settings.html", form=form, university=university)
