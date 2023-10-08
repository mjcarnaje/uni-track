from flask import Blueprint, jsonify, render_template, request, redirect

from .. import db
from ..models.College import College
from ..models.Course import Course

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
def colleges():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    college_query = College().find_all(
        page_number=page,
        page_size=2,
        query=query
    )

    colleges = college_query.get("data")
    has_previous_page = college_query.get("has_previous_page")
    has_next_page = college_query.get("has_next_page")

    return render_template("colleges.html", colleges=colleges, page=page, has_previous_page=has_previous_page, has_next_page=has_next_page, query=query)


@college_bp.route("/add", methods=["GET", "POST"])
def add_college():
    if request.method == "POST":
        college = College(
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=request.form.get('photo')
        )

        college.insert()

        return redirect("/college/")

    return render_template("add-college.html")


@college_bp.route("/update/<int:id>", methods=["GET", "POST"])
def update_college(id):
    college_query = College(id=id)

    if request.method == "POST":
        updated_college = College(
            id=id,
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=request.form.get('photo')
        )

        updated_college.update()

        return redirect("/college/")

    college = college_query.find_one()

    return render_template("update-college.html", college=college)


@college_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def college(id):
    college_query = College(id=id)

    if request.method == "DELETE":
        college_query.delete()
        return jsonify({'success': True})

    college = college_query.find_one()
    courses = college_query.find_courses()

    return render_template("college.html", college=college, courses=courses)
