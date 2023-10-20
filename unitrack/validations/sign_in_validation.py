from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, validators
from ..models.University import University
from werkzeug.security import check_password_hash


class SignInValidation(FlaskForm):
    email = StringField('Email Address', [
        validators.DataRequired("Please enter your email address."),
    ])
    password = PasswordField('Password', [
        validators.DataRequired("Please enter a password."),
    ])

    def validate_email(self, field):
        if not University.check_if_email_exists(field.data):
            raise validators.ValidationError(
                'Email address does not exist')

    def validate_password(self, field):
        university = University.find_by_email(email=self.email.data)

        if university and not check_password_hash(university.password, field.data):
            raise validators.ValidationError(
                'Password is incorrect')
