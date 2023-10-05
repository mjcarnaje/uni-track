from flask import Blueprint, jsonify, render_template, request

from .. import db
from ..models.College import College
from ..models.Course import Course

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
def colleges():
    colleges = db.session.execute(
        db.select(College).order_by(College.name)).scalars().all()
    return render_template("colleges.html", colleges=colleges)


@college_bp.route("/add")
def add_college():
    return render_template("add-college.html")


@college_bp.route('/<int:id>', methods=['GET', 'POST', 'DELETE'])
def college(id):
    if request.method == "DELETE":
        college = College.query.get(id)
        db.session.delete(college)
        db.session.commit()
        return jsonify({'success': True})

    if request.method == "POST":
        return jsonify({'success': True})

    college = College.query.get(id)
    courses = db.session.execute(
        db.select(Course).filter_by(college_id=id)).scalars().all()

    return render_template("college.html", college=college, courses=courses)
