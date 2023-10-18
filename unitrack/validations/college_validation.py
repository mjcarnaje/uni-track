from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, validators, HiddenField
from ..models.College import College


class BaseCollegeValidation(FlaskForm):
    name = StringField('Name', [
        validators.Length(min=4, max=256)
    ])
    code = StringField('Code', [
        validators.Length(min=3, max=16)
    ])


class AddCollegeValidation(BaseCollegeValidation):
    photo = FileField('Photo', validators=[
        FileRequired()
    ])

    def validate_code(self, code):
        if College.check_if_code_exists(code.data):
            raise validators.ValidationError('Code already exists')


class UpdateCollegeValidation(BaseCollegeValidation):
    id = HiddenField('Id')
    photo = FileField('Photo')

    def validate_code(self, code):
        if College.check_if_code_exists(code.data, self.id.data):
            raise validators.ValidationError('Code already exists')
