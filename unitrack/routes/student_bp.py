import os

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, redirect, render_template, request
from flask_login import current_user, login_required

from unitrack.utils.upload_file import save_file, save_file_wtf

from ..models.College import College
from ..models.Course import Course
from ..models.Student import Student

from ..validations import AddStudentValidation, UpdateStudentValidation

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
@login_required
def students():
    page = request.args.get('page', 1, type=int)

    query = request.args.get('query', '', type=str)
    college_id = request.args.get('college_id', '', type=int)
    course_id = request.args.get('course_id', '', type=int)
    gender = request.args.get('gender', '', type=str)

    students_query = Student(university_id=current_user.id).find_all(
        page_number=page,
        page_size=12,
        query=query,
        college_id=college_id,
        course_id=course_id,
        gender=gender,
    )

    students = students_query.get("data")
    has_previous_page = students_query.get("has_previous_page")
    has_next_page = students_query.get("has_next_page")
    total_count = students_query.get("total_count")

    colleges = College(university_id=current_user.id).find_all().get("data")

    courses = []
    filters = {
        'gender': None,
        'college': None,
        'course': None
    }

    if gender:
        filters["gender"] = {
            'key': 'gender',
            'name': gender
        }

    if college_id:
        college = College(id=college_id).find_one()
        courses = College(id=college.get("id")).find_courses()
        filters["college"] = {'key': 'college_id', **college}

        if course_id:
            course = Course(id=course_id).find_one()
            filters["course"] = {'key': 'course_id', **course}

    return render_template("students.html",
                           students=students,
                           colleges=colleges,
                           courses=courses,
                           page=page,
                           has_previous_page=has_previous_page,
                           has_next_page=has_next_page,
                           total_count=total_count,
                           query=query,
                           filters=filters,
                           show_filters=len(
                               list(filter(lambda filter: filter, filters.values()))) > 0
                           )


@student_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    colleges = College(university_id=current_user.id).find_all().get("data")
    form = AddStudentValidation()
    college_choices = [(college.get("id"), college.get("name"))
                       for college in colleges]
    form.college_id.choices = college_choices
    form.course_id.choices = []
    if (form.college_id.data):
        courses = College(id=form.college_id.data,
                          university_id=current_user.id).find_courses()
        course_choices = [(course.get("id"), course.get("name"))
                          for course in courses]
        form.course_id.choices = course_choices

    if form.validate_on_submit():
        student = Student(
            student_id=form.student_id.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            birthday=form.birthday.data,
            college_id=request.form.get('college_id'),
            course_id=request.form.get('course_id'),
            photo=save_file_wtf(data=form.photo.data),
            university_id=current_user.id
        )

        student.insert()

        return redirect("/student/")

    return render_template("add-student.html", form=form, colleges=colleges)


@student_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_student(id):
    student_query = Student(id=id, university_id=current_user.id)
    student = student_query.find_one()

    if request.method == "POST":
        student_query.student_id = request.form.get('student_id')
        student_query.first_name = request.form.get('first_name')
        student_query.last_name = request.form.get('last_name')
        student_query.gender = request.form.get('gender')
        student_query.birthday = request.form.get('birthday')
        student_query.photo = request.form.get('photo')
        student_query.college_id = request.form.get('college_id')
        student_query.course_id = request.form.get('course_id')
        student_query.photo = save_file(key='photo') or student.photo

        student_query.update()

        return redirect("/student")

    colleges = College(university_id=current_user.id).find_all().get("data")
    courses = College(id=student.get('college_id'),
                      university_id=current_user.id).find_courses()

    return render_template("update-student.html", student=student, colleges=colleges, courses=courses)


@student_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def student(id):
    student_query = Student(id=id, university_id=current_user.id)
    student = student_query.find_one()

    # TODO: Separate this into a different route
    if request.method == "DELETE":
        student_query.delete()

        student_photo = student.get("photo")

        if student_photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], student_photo)) and student_photo != "default.png":
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], student_photo))

        return jsonify({'success': True})

    return render_template("student.html", student=student)
