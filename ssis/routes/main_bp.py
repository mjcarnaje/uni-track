from flask import Blueprint
from flask import redirect, url_for

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def dashboard():
    return redirect(url_for('student.students'))
