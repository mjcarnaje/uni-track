import os

from flask import Blueprint
from flask import current_app as app
from flask import jsonify, redirect, render_template, request
from flask_login import login_required

from ..models.College import College
from ..utils.upload_file import save_file

college_bp = Blueprint('college', __name__)


@college_bp.route('/')
def colleges():
    page = request.args.get('page', 1, type=int)
    query = request.args.get('query', '', type=str)

    college_query = College().find_all(
        page_number=page,
        page_size=12,
        query=query
    )

    colleges = college_query.get("data")
    has_previous_page = college_query.get("has_previous_page")
    has_next_page = college_query.get("has_next_page")
    total_count = college_query.get("total_count")

    return render_template("colleges.html",
                           colleges=colleges,
                           page=page,
                           has_previous_page=has_previous_page,
                           has_next_page=has_next_page,
                           total_count=total_count,
                           query=query,
                           )


@college_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_college():
    if request.method == "POST":
        college_query = College(
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=save_file(key='photo')
        )

        college_query.insert()

        return redirect("/college/")

    return render_template("add-college.html")


@college_bp.route("/update/<int:id>", methods=["GET", "POST"])
@login_required
def update_college(id):
    college_query = College(id=id)

    if request.method == "POST":
        updated_college = College(
            id=id,
            name=request.form.get('name'),
            code=request.form.get('code'),
            photo=save_file(key='photo')
        )

        updated_college.update()

        return redirect("/college/")

    college = college_query.find_one()

    return render_template("update-college.html", college=college)


@college_bp.route('/<int:id>', methods=['GET', 'DELETE'])
def college(id):
    college_query = College(id=id)
    college = college_query.find_one()

    # TODO: Separate this into a different route
    if request.method == "DELETE":
        res = college_query.delete()
        print(f"result: {res}")
        college_photo = college.get('photo')

        if college_photo and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], college_photo)):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], college_photo))

        return jsonify({'success': True})

    courses = college_query.find_courses()

    return render_template("college.html", college=college, courses=courses)
