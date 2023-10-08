from flask import Blueprint
from flask import render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    return render_template("home.html")
