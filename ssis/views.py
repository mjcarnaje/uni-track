from flask import Blueprint, render_template

views_blue_print = Blueprint('view', __name__)


@views_blue_print.route('/')
def dashboard():
    return render_template("home.html")
