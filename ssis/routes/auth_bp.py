from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.User import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            return redirect(url_for('auth.signup'))

        user = User(username=username,
                    email=email,
                    password=generate_password_hash(password=password, method='sha256'))

        if user.find_by_username() or user.find_by_email():
            return redirect(url_for('auth.signup'))

        user.create()

        return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User(email=email).find_by_email()

        if not user:
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            return redirect(url_for('auth.login'))

        login_user(user, remember=True)

        return redirect(url_for('main.dashboard'))

    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
