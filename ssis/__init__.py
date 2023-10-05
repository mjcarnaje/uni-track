from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DBNAME = "ssis"
UPLOAD_FOLDER = 'ssis/static/uploads'
SECRET_KEY = 'this-is-a-secret-key'


def create_database(app: Flask):
    with app.app_context():
        db.create_all()
    print("Database Created!")


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/ssis'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)

    from ssis.routes.auth_bp import auth_bp
    from ssis.routes.college_bp import college_bp
    from ssis.routes.student_bp import student_bp
    from ssis.routes.main_bp import main_bp
    from ssis.routes.course_bp import course_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/student/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(auth_bp, url_prefix='/auth/')

    from .models.College import College
    from .models.Course import Course
    from .models.Student import Student

    create_database(app)

    return app
