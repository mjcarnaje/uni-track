from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, validators


class CollegeValidation(FlaskForm):
    photo = FileField('Logo', validators=[
                      FileRequired('Please upload a logo.')])
    name = StringField('Name', [
        validators.Length(min=4, max=256)
    ])
    code = StringField('Code', [
        validators.Length(min=4, max=16)
    ])
