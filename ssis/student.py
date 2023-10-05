from flask import Blueprint, render_template, jsonify
from . import db
from .models import Student

student_bp = Blueprint('student', __name__)


@student_bp.route('/')
def students():
    students = db.session.execute(
        db.select(Student).order_by(Student.first_name)).scalars().all()
    return render_template("students.html", students=students)


@student_bp.route('/<int:id>', methods=['DELETE'])
def student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return jsonify({'success': True})
