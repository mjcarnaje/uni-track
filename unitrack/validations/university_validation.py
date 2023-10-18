from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, PasswordField, validators, widgets


def should_be_not_equal(form, field):
    if field.data == form.primary_color.data:
        raise validators.ValidationError(
            'Choose a different color than primary color.')


class UniversityValidation(FlaskForm):
    logo = FileField('Logo', validators=[FileRequired()])
    email = StringField('Email Address', [
        validators.Length(min=6, max=35)
    ])
    display_name = StringField('Display Name', [
        validators.Length(min=4, max=25)
    ])
    name = StringField('Name', [
        validators.Length(min=4, max=25)
    ])
    primary_color = StringField('Primary Color', [
        validators.Length(min=6, message='Choose color'),
    ],
        widget=widgets.ColorInput()
    )
    secondary_color = StringField('Secondary Color', [
        validators.Length(min=6, message='Choose color'),
        should_be_not_equal
    ],
        widget=widgets.ColorInput()
    )
    password = PasswordField('New Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [
        validators.Length(min=8, max=25),
        validators.EqualTo('password', message='Passwords must match')
    ])
