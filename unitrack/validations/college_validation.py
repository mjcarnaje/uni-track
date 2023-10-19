from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, validators, HiddenField
from ..models.College import College
from flask_login import current_user


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
        if College(university_id=current_user.id).check_if_code_exists(code=code.data):
            raise validators.ValidationError(
                'Code already exists in this university')

    def validate_name(self, name):
        if College(university_id=current_user.id).check_if_name_exists(name=name.data):
            raise validators.ValidationError(
                'Name already exists in this university')


class UpdateCollegeValidation(BaseCollegeValidation):
    id = HiddenField('Id')
    photo = FileField('Photo')

    def validate_code(self, code):
        if College(university_id=current_user.id).check_if_code_exists(code=code.data, id=self.id.data):
            raise validators.ValidationError(
                'Code already exists in this university')

    def validate_name(self, name):
        if College(university_id=current_user.id).check_if_name_exists(name=name.data, id=self.id.data):
            raise validators.ValidationError(
                'Name already exists in this university')
