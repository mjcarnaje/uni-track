from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.University import University
from ..utils.upload_file import save_file

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        display_name = request.form.get('display_name')
        name = request.form.get('name')
        primary_color = request.form.get('primary_color')
        secondary_color = request.form.get('secondary_color')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return redirect(url_for('auth.signup'))

        university = University(
            email=email,
            logo=save_file(key='logo'),
            display_name=display_name,
            name=name,
            primary_color=primary_color,
            secondary_color=secondary_color,
            password=generate_password_hash(password=password))

        if university.find_by_email():
            return redirect(url_for('auth.signup'))

        university.create()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        university = University(email=email).find_by_email()

        if not university:
            return redirect(url_for('auth.login'))

        if not check_password_hash(university.password, password):
            return redirect(url_for('auth.login'))

        login_user(university, remember=True)

        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
