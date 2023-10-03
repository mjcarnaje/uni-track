from flask import Blueprint, render_template, jsonify
from . import db
from .models import Student

student_blue_print = Blueprint('student', __name__)


@student_blue_print.route('/')
def students():
    students = db.session.execute(
        db.select(Student).order_by(Student.first_name)).scalars().all()
    return render_template("students.html", students=students)


@student_blue_print.route('/<int:id>', methods=['DELETE'])
def student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'success': True})
