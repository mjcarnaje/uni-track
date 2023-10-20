from flask_wtf import FlaskForm
from wtforms import StringField, validators, HiddenField, SelectField, DateField
from ..models.Student import Student
from flask_login import current_user


class StudentValidationMixin:
    photo = StringField('Photo', validators=[validators.DataRequired()])
    student_id = StringField('Student ID', [
        validators.Length(min=4, max=16)
    ])
    first_name = StringField('First Name', [
        validators.Length(min=4, max=256)
    ])
    last_name = StringField('Last Name', [
        validators.Length(min=4, max=256)
    ])
    gender = SelectField('Gender', choices=[
                         ("Male", "Male"), ("Female", "Female"), ("Other", "Other")])
    birthday = DateField('Birthday', format='%Y-%m-%d')
    college_id = SelectField('College', validators=[
                             validators.DataRequired()], coerce=int, validate_choice=False)
    course_id = SelectField('Course',  validators=[
                            validators.DataRequired()], coerce=int, validate_choice=False)


class AddStudentValidation(FlaskForm, StudentValidationMixin):
    def validate_student_id(self, student_id):
        if Student.check_if_student_id_exists(student_id=student_id.data, university_id=current_user.id):
            raise validators.ValidationError(
                'Student ID already exists in this university')


class UpdateStudentValidation(FlaskForm, StudentValidationMixin):
    id = HiddenField('Id')

    def validate_student_id(self, student_id):
        if Student.check_if_student_id_exists(student_id=student_id.data, university_id=current_user.id, id=self.id.data):
            raise validators.ValidationError(
                'Student ID already exists in this university')
