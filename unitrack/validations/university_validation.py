from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, validators, widgets, HiddenField
from ..models.University import University


class BaseUniversityValidation(FlaskForm):
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


class AddUniversityValidation(BaseUniversityValidation):
    logo = FileField('Logo', validators=[FileRequired()])

    password = PasswordField('New Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('password', message='Passwords must match')
    ])

    def validate_email(self, field):
        university = University.check_if_email_exists(field.data)
        if university:
            raise validators.ValidationError(
                'Email address already exists')


class UpdateUniversityValidation(BaseUniversityValidation):
    id = HiddenField('ID')
    logo = FileField('Logo')

    def validate_email(self, field):
        university = University.check_if_email_exists(field.data, self.id.data)
        if university:
            raise validators.ValidationError(
                'Email address already exists')
