from flask_wtf import FlaskForm
from wtforms import StringField, validators, HiddenField
from ..models.Course import Course
from flask_login import current_user


class CourseValidationMixin:
    photo = StringField('Photo', [validators.DataRequired()])
    name = StringField('Name', [
        validators.Length(min=4, max=256)
    ])
    code = StringField('Code', [
        validators.Length(min=3, max=16)
    ])


class AddCourseValidation(FlaskForm, CourseValidationMixin):
    def validate_code(self, code):
        if Course.check_if_code_exists(code=code.data, university_id=current_user.id):
            raise validators.ValidationError(
                'Code already exists in this university')

    def validate_name(self, name):
        if Course.check_if_name_exists(name=name.data, university_id=current_user.id):
            raise validators.ValidationError(
                'Name already exists in this university')


class UpdateCourseValidation(FlaskForm, CourseValidationMixin):
    id = HiddenField('Id')

    def validate_code(self, code):
        if Course.check_if_code_exists(code=code.data, university_id=current_user.id, id=self.id.data):
            raise validators.ValidationError(
                'Code already exists in this university')

    def validate_name(self, name):
        if Course.check_if_name_exists(name=name.data, university_id=current_user.id, id=self.id.data):
            raise validators.ValidationError(
                'Name already exists in this university')
