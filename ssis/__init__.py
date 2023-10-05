from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DBNAME = "ssis"


def create_database(app: Flask):
    with app.app_context():
        db.create_all()
    print("Database Created!")


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/ssis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .views import views_blue_print
    from .student import student_blue_print
    from .auth import auth_blue_print
    from .college import college_blue_print
    from .course import course_blue_print

    app.register_blueprint(views_blue_print, url_prefix='/')
    app.register_blueprint(student_blue_print, url_prefix='/student/')
    app.register_blueprint(college_blue_print, url_prefix='/college/')
    app.register_blueprint(course_blue_print, url_prefix='/course/')
    app.register_blueprint(auth_blue_print, url_prefix='/auth/')

    from .models import Student, Course, College

    create_database(app)

    return app
