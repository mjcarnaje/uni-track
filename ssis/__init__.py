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

    from .views import views_bp
    from .student import student_bp
    from .auth import auth_bp
    from .college import college_bp
    from .course import course_bp

    app.register_blueprint(views_bp, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/student/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(auth_bp, url_prefix='/auth/')

    from .models import Student, Course, College

    create_database(app)

    return app
