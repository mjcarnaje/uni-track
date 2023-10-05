from flask import Blueprint, render_template

views_bp = Blueprint('view', __name__)


@views_bp.route('/')
def dashboard():
    return render_template("home.html")
