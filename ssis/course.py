from flask import Blueprint, jsonify, request, redirect
from . import db
from .models import Course

course_blue_print = Blueprint('course', __name__)


@course_blue_print.route('/', methods=['POST'])
def courses():
    if request.method == "POST":
        course = Course()
        course.name = request.form.get('name')
        course.code = request.form.get('code')
        course.photo = request.form.get('photo')
        course.college_id = request.form.get('college_id')
        db.session.add(course)
        db.session.commit()
        return redirect(f'/college/{course.college_id}')


@course_blue_print.route('/<int:id>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def course(id):
    if request.method == "POST":
        course = Course.query.get(id)
        course.name = request.form.get('name')
        course.code = request.form.get('code')
        course.photo = request.form.get('photo')
        db.session.commit()
        return redirect(f'/college/{course.college_id}')

    if request.method == "DELETE":
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return jsonify({'success': True})
