
from flask import Blueprint, jsonify, redirect, render_template, request
from flask_login import current_user, login_required

from ..models.College import College
from ..models.Course import Course
from ..validations import (AddCollegeValidation, AddCourseValidation,
                           UpdateCollegeValidation, UpdateCourseValidation)

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
@login_required
def colleges():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    college_query = College.find_all(
        university_id=current_user.id,
        page_number=page,
        page_size=12,
        query=query
    )

    colleges = college_query.get("data")
    has_previous_page = college_query.get("has_previous_page")
    has_next_page = college_query.get("has_next_page")
    total_count = college_query.get("total_count")

    return render_template("colleges.html",
                           colleges=colleges,
                           page=page,
                           has_previous_page=has_previous_page,
                           has_next_page=has_next_page,
                           total_count=total_count,
                           query=query,
                           )


@college_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_college():
    form = AddCollegeValidation()

    if form.validate_on_submit():
        College.insert(name=form.name.data, code=form.code.data,
                       photo=form.photo.data, university_id=current_user.id)

        return redirect("/college/")

    return render_template("add-college.html", form=form)


@college_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_college(id):
    college = College.find_by_id(id=id, university_id=current_user.id)

    form = UpdateCollegeValidation()

    if form.validate_on_submit():
        College.update(id=id, name=form.name.data,
                       code=form.code.data, photo=form.photo.data, university_id=current_user.id)
        return redirect("/college/")

    form.id.data = college.id
    form.name.data = college.name
    form.code.data = college.code
    form.photo.data = college.photo

    return render_template("update-college.html", form=form, college=college)


@college_bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_college(id):
    College.delete(id=id, university_id=current_user.id)
    return jsonify({'success': True, 'message': "College successfuly deleted."})


@college_bp.route('/<string:id>', methods=['GET', 'DELETE', "POST"])
@login_required
def view_college(id):
    college = College.find_by_id(id=id, university_id=current_user.id)
    courses = Course.find_by_college_id(
        university_id=current_user.id, college_id=id)

    return render_template("college.html", college=college, courses=courses)


@college_bp.route('/<string:id>/add-course', methods=['GET', 'POST'])
@login_required
def add_course(id):
    form = AddCourseValidation()

    if form.validate_on_submit():
        Course.insert(college_id=id, name=form.name.data, code=form.code.data,
                      photo=form.photo.data, university_id=current_user.id)

        return redirect(f"/college/{id}")

    return render_template("add-course.html", form=form)


@college_bp.route('/<int:college_id>/update-course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(college_id, course_id):
    course = Course.find_by_id(university_id=current_user.id, id=course_id)

    form = UpdateCourseValidation()

    if form.validate_on_submit():
        Course.update(id=college_id, name=form.name.data, code=form.code.data,
                      photo=form.photo.data,
                      college_id=college_id,
                      university_id=current_user.id)
        return redirect(f"/college/{college_id}")

    form.id.data = course.id
    form.name.data = course.name
    form.code.data = course.code
    form.photo.data = course.photo

    return render_template("update-course.html", form=form, course=course)
