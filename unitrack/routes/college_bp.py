import os

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, redirect, render_template, request
from flask_login import current_user, login_required

from ..models.College import College
from ..models.Course import Course
from ..utils.upload_file import save_file_wtf
from ..validations import AddCollegeValidation, AddCourseValidation, UpdateCollegeValidation, UpdateCourseValidation

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
@login_required
def colleges():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    college_query = College(university_id=current_user.id).find_all(
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
        college_query = College(
            name=form.name.data,
            code=form.code.data,
            photo=save_file_wtf(data=form.photo.data),
            university_id=current_user.id
        )

        college_query.insert()

        return redirect("/college/")

    return render_template("add-college.html", form=form)


@college_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_college(id):
    college_query = College(id=id, university_id=current_user.id)
    college = college_query.find_one()

    form = UpdateCollegeValidation()

    if form.validate_on_submit():
        college_query.name = form.name.data
        college_query.code = form.code.data
        college_query.photo = save_file_wtf(
            data=form.photo.data,
            default_filename=college.get("photo"))
        college_query.update()
        return redirect("/college/")

    form.id.data = college.get("id")
    form.name.data = college.get("name")
    form.code.data = college.get("code")
    form.photo.data = college.get("photo")

    return render_template("update-college.html", form=form, college=college)


@college_bp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
def delete_college(id):
    college_query = College(id=id, university_id=current_user.id)
    college = college_query.find_one()
    college_photo = college.get('photo')

    college_query.delete()

    if college_photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], college_photo)):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], college_photo))

    return jsonify({"success": True})


@college_bp.route('/<string:id>', methods=['GET', 'DELETE', "POST"])
@login_required
def view_college(id):
    college_query = College(id=id, university_id=current_user.id)
    college = college_query.find_one()
    courses = college_query.find_courses()

    return render_template("college.html", college=college, courses=courses)


@college_bp.route('/<string:id>/add-course', methods=['GET', 'POST'])
@login_required
def add_course(id):
    form = AddCourseValidation()

    if form.validate_on_submit():
        course_query = Course(
            name=form.name.data,
            code=form.code.data,
            photo=save_file_wtf(data=form.photo.data),
            college_id=id,
            university_id=current_user.id
        )

        course_query.insert()

        return redirect(f"/college/{id}")

    return render_template("add-course.html", form=form)


@college_bp.route('/<int:college_id>/update-course/<int:course_id>', methods=['GET', 'POST'])
@login_required
def update_course(college_id, course_id):
    course_query = Course(id=course_id, college_id=college_id,
                          university_id=current_user.id)
    course = course_query.find_one()

    form = UpdateCourseValidation()

    if form.validate_on_submit():
        course_query.name = form.name.data
        course_query.code = form.code.data
        course_query.photo = save_file_wtf(
            data=form.photo.data,
            default_filename=course.get("photo"))
        course_query.update()
        return redirect(f"/college/{college_id}")

    form.id.data = course.get("id")
    form.name.data = course.get("name")
    form.code.data = course.get("code")
    form.photo.data = course.get("photo")

    return render_template("update-course.html", form=form, course=course)
