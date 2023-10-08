import os
from flask import Blueprint, render_template, request, redirect, current_app as app, jsonify

from ssis.utils.upload_file import save_file


from ..models.Student import Student
from ..models.College import College
from ..models.Course import Course

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
def students():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)
    college_id = request.args.get('college_id', '', type=int)
    course_id = request.args.get('course_id', '', type=int)

    students_query = Student().find_all(
        page_number=page,
        page_size=2,
        query=query,
        college_id=college_id,
        course_id=course_id
    )

    students = students_query.get("data")
    has_previous_page = students_query.get("has_previous_page")
    has_next_page = students_query.get("has_next_page")

    colleges = College().find_all(
        page_number=1,
        page_size=100,
        query=""
    ).get("data")

    courses = Course().find_by_college_id(college_id) if college_id else []

    return render_template("students.html", students=students, colleges=colleges, courses=courses, page=page, has_previous_page=has_previous_page, has_next_page=has_next_page, query=query, college_id=college_id, course_id=course_id)


@student_bp.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = Student(
            student_id=request.form.get('student_id'),
            first_name=request.form.get('first_name'),
            last_name=request.form.get('last_name'),
            gender=request.form.get('gender'),
            birthday=request.form.get('birthday'),
            college_id=request.form.get('college_id'),
            course_id=request.form.get('course_id'),
            photo=save_file(key='photo') or 'default.png'
        )

        student.insert()

        return redirect("/student/")

    colleges = College().find_all().get("data")

    print(colleges)

    return render_template("add-student.html", colleges=colleges)


@student_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    student_query = Student(id=id)
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
        student_query.photo = save_file(key='photo') or student_query.photo
        student_query.update()
        return redirect("/student")

    colleges = College().find_all().get("data")
    courses = College(id=student.get('college').get('id')).find_courses()

    return render_template("update-student.html", student=student, colleges=colleges, courses=courses)


@student_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def student(id):
    student_query = Student(id=id)
    student = student_query.find_one()

    if request.method == "DELETE":
        student_query.delete()

        if student.get("photo") and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], student.get("photo"))):
            os.remove(os.path.join(
                app.config['UPLOAD_FOLDER'], student.get("photo")))

        return jsonify({'success': True})

    return render_template("student.html", student=student)
