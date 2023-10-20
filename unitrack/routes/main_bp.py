from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required

from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student
from ..models.University import University

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
        University.update(id=current_user.id, email=form.email.data, logo=form.data.logo, name=form.name.data,
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
