from flask import Blueprint, jsonify, render_template, request, redirect

from .. import db
from ..models.Student import Student
from ..models.College import College
from ..models.Course import Course

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
def students():
    students = db.session.execute(
        db.select(Student).order_by(Student.first_name)).scalars().all()
    return render_template("students.html", students=students)


@student_bp.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        student = Student()
        student.student_id = request.form.get('student_id')
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.gender = request.form.get('gender')
        student.birthday = request.form.get('birthday')
        student.photo = request.form.get('photo')
        student.college_id = request.form.get('college_id')
        student.course_id = request.form.get('course_id')
        db.session.add(student)
        db.session.commit()
        return redirect("/student/")

    colleges = College.query.all()

    return render_template("add-student.html", colleges=colleges)


@student_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    student = Student.query.get(id)

    if request.method == "POST":
        student.student_id = request.form.get('student_id')
        student.first_name = request.form.get('first_name')
        student.last_name = request.form.get('last_name')
        student.gender = request.form.get('gender')
        student.birthday = request.form.get('birthday')
        student.photo = request.form.get('photo')
        student.college_id = request.form.get('college_id')
        student.course_id = request.form.get('course_id')
        db.session.commit()
        return redirect("/student")

    colleges = College.query.all()
    courses = Course.query.filter_by(college_id=student.college_id).all()

    return render_template("update-student.html", student=student, colleges=colleges, courses=courses)


@student_bp.route('/<int:id>', methods=['DELETE'])
def student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'success': True})
