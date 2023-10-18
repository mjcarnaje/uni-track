from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class SignInValidation(FlaskForm):
    email = StringField('Email Address', [
        validators.DataRequired("Please enter your email address."),
    ])
    password = PasswordField('Password', [
        validators.DataRequired("Please enter a password."),
    ])
