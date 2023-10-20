from flask import Blueprint
from flask import jsonify, redirect, render_template, request
from flask_login import current_user, login_required

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

    students_query = Student.find_all(
        university_id=current_user.id,
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

    colleges = College.find_all(university_id=current_user.id).get("data")

    courses = []
    filters = {
        'gender': None,
        'college': None,
        'course': None
    }
    show_filters = False

    if gender:
        show_filters = True
        filters["gender"] = {
            'key': 'gender',
            'name': gender
        }

    if college_id:
        show_filters = True
        college = College.find_by_id(
            university_id=current_user.id, id=college_id)
        courses = Course.find_by_college_id(
            university_id=current_user.id, college_id=college_id)

        filters["college"] = {'key': 'college_id', **college}

        if course_id:
            course = Course.find_by_id(course_id)
            filters["course"] = {'key': 'course_id', **course}

    can_add_student = Course.count(university_id=current_user.id) > 0

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
                           show_filters=show_filters,
                           can_add_student=can_add_student
                           )


@student_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    can_add_student = Course.count(university_id=current_user.id) > 0

    if not can_add_student:
        return redirect("/student/")

    form = AddStudentValidation()

    colleges = College.find_all(university_id=current_user.id).get("data")
    college_choices = [(college.get("id"), college.get("name"))
                       for college in colleges]

    form.college_id.choices = college_choices
    form.course_id.choices = []

    if (form.college_id.data):
        courses = Course.find_by_college_id(
            university_id=current_user.id, college_id=form.college_id.data)
        course_choices = [(course.get("id"), course.get("name"))
                          for course in courses]
        form.course_id.choices = course_choices

    if form.validate_on_submit():
        Student.insert(student_id=form.student_id.data, first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data,
                       birthday=form.birthday.data, photo=form.photo.data, year_enrolled=form.year_enrolled.data, college_id=form.college_id.data, course_id=form.course_id.data, university_id=current_user.id)

        return redirect("/student/")

    return render_template("add-student.html", form=form, colleges=colleges)


@student_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_student(id):
    student = Student.find_by_id(id=id, university_id=current_user.id)

    form = UpdateStudentValidation()

    colleges = College.find_all(university_id=current_user.id).get("data")
    college_choices = [(college.get("id"), college.get("name"))
                       for college in colleges]

    form.college_id.choices = college_choices
    form.course_id.choices = []

    if form.validate_on_submit():
        Student.update(id=id, student_id=form.student_id.data, first_name=form.first_name.data, last_name=form.last_name.data, gender=form.gender.data,
                       birthday=form.birthday.data, photo=form.photo.data, year_enrolled=form.year_enrolled.data, college_id=form.college_id.data, course_id=form.course_id.data, university_id=current_user.id)
        return redirect("/student")

    form.id.data = student.id
    form.student_id.data = student.student_id
    form.first_name.data = student.first_name
    form.last_name.data = student.last_name
    form.gender.data = student.gender
    form.birthday.data = student.birthday
    form.photo.data = student.photo
    form.year_enrolled.data = student.year_enrolled
    form.college_id.data = student.college_id
    form.course_id.data = student.course_id

    if (form.college_id.data):
        courses = Course.find_by_college_id(
            university_id=current_user.id, college_id=form.college_id.data)
        course_choices = [(course.get("id"), course.get("name"))
                          for course in courses]
        form.course_id.choices = course_choices

    return render_template("update-student.html", form=form, student=student)


@student_bp.route('/<int:id>')
def view_student(id):
    student = Student.find_by_id(id=id, university_id=current_user.id)
    return render_template("student.html", student=student)


@student_bp.route('/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_student(id):
    Student.delete(id=id, university_id=current_user.id)
    return jsonify({"success": True})
