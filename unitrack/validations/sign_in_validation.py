from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators


class SignInValidation(FlaskForm):
    email = StringField('Email Address', [
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('Password', [
        validators.Length(min=8, max=25)
    ])
