from flask import Blueprint, jsonify, render_template, request, redirect
from sqlalchemy.sql.operators import ilike_op

from .. import db
from ..models.College import College
from ..models.Course import Course

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
def colleges():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    college_query = College.query

    if query:
        college_query = college_query.filter(
            ilike_op(College.name, f"%{query}%"))

    college_query = college_query.paginate(page=page, per_page=10)

    return render_template("colleges.html", colleges=college_query.items, page=page, has_previous_page=college_query.has_prev, has_next_page=college_query.has_next, query=query)


@college_bp.route("/add", methods=["GET", "POST"])
def add_college():
    if request.method == "POST":
        college = College()
        college.name = request.form.get('name')
        college.code = request.form.get('code')
        college.photo = request.form.get('photo')
        db.session.add(college)
        db.session.commit()
        return redirect("/college/")

    return render_template("add-college.html")


@college_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_college(id):
    college = College.query.get(id)

    if request.method == "POST":
        college.name = request.form.get('name')
        college.code = request.form.get('code')
        college.photo = request.form.get('photo')
        db.session.commit()
        return redirect("/college/")

    return render_template("update-college.html", college=college)


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
