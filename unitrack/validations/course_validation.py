from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, validators, HiddenField
from ..models.Course import Course
from flask_login import current_user


class BaseCourseValidation(FlaskForm):
    id = HiddenField('Id')

    name = StringField('Name', [
        validators.Length(min=4, max=256)
    ])
    code = StringField('Code', [
        validators.Length(min=3, max=16)
    ])
    college_id = HiddenField('College Id')


class AddCourseValidation(BaseCourseValidation):
    photo = FileField('Photo', validators=[
        FileRequired()
    ])

    def validate_code(self, code):
        print("AddCourseValidation")
        if Course(university_id=current_user.id).check_if_code_exists(code=code.data):
            raise validators.ValidationError('Code already exists')


class UpdateCourseValidation(BaseCourseValidation):
    photo = FileField('Photo')

    def validate_code(self, code):
        print("UpdateCourseValidation")
        if Course(university_id=current_user.id).check_if_code_exists(code=code.data, id=self.id.data):
            raise validators.ValidationError('Code already exists')
