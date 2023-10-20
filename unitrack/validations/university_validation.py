from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, HiddenField, validators, widgets
from ..models.University import University


class UniversityValidationMixin:
    logo = StringField('Logo', [validators.DataRequired()])
    email = StringField('Email Address', [
        validators.Length(min=6, max=64)
    ])
    display_name = StringField('Display Name', [
        validators.Length(min=4, max=25)
    ])
    name = StringField('Name', [
        validators.Length(min=4, max=128)
    ])
    primary_color = StringField('Primary Color', [
        validators.Length(min=6, message='Choose color'),
    ],
        widget=widgets.ColorInput()
    )
    secondary_color = StringField('Secondary Color', [
        validators.Length(min=6, message='Choose color'),
    ],
        widget=widgets.ColorInput()
    )

    def validate_secondary_color(self, field):
        if field.data == self.primary_color.data:
            raise validators.ValidationError(
                'Primary and Secondary colors should not be the same')


class AddUniversityValidation(FlaskForm, UniversityValidationMixin):
    password = PasswordField('New Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('password', message='Passwords must match')
    ])

    def validate_email(self, field):
        if University.check_if_email_exists(field.data):
            raise validators.ValidationError('Email address already exists')


class UpdateUniversityValidation(FlaskForm, UniversityValidationMixin):
    id = HiddenField('ID')

    def validate_email(self, field):
        if University.check_if_email_exists(field.data, self.id.data):
            raise validators.ValidationError('Email address already exists')
