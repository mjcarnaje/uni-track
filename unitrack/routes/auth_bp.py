from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.University import University
from ..utils.upload_file import save_file_wtf
from ..validations import SignInValidation, UniversityValidation

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UniversityValidation()

    if request.method == 'POST' and form.validate_on_submit():
        university = University(
            email=form.email.data,
            logo=save_file_wtf(data=form.logo.data),
            display_name=form.display_name.data,
            name=form.display_name.data,
            primary_color=form.primary_color.data,
            secondary_color=form.secondary_color.data,
            password=generate_password_hash(password=form.password.data))

        if university.find_by_email():
            return redirect(url_for('auth.signup'))

        university.insert()

        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInValidation()

    if request.method == 'POST' and form.validate_on_submit():
        university = University(email=form.email.data).find_by_email()

        if not university:
            return redirect(url_for('auth.login'))

        if not check_password_hash(university.password, form.password.data):
            return redirect(url_for('auth.login'))

        login_user(university, remember=True)

        return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
