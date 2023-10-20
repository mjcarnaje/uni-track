from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.University import University
from ..validations import AddUniversityValidation, SignInValidation

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = AddUniversityValidation()

    if form.validate_on_submit():
        University.insert(email=form.email.data, logo=form.logo.data, display_name=form.display_name.data, name=form.display_name.data,
                          primary_color=form.primary_color.data, secondary_color=form.secondary_color.data, password=generate_password_hash(form.password.data))

        return redirect(url_for('main.dashboard'))

    return render_template('signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = SignInValidation()

    if form.validate_on_submit():
        university = University.find_by_email(email=form.email.data)

        login_user(university, remember=True)

        return redirect(url_for('main.dashboard'))

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
