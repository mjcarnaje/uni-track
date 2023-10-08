from flask import Flask
from flask_mysql_connector import MySQL, Params

from .db import create_tables

UPLOAD_FOLDER = 'ssis/static/uploads'
SECRET_KEY = 'this-is-a-secret-key'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'ssis'


mysql = MySQL()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config[Params.MYSQL_HOST] = MYSQL_HOST
    app.config[Params.MYSQL_USER] = MYSQL_USER
    app.config[Params.MYSQL_PASSWORD] = MYSQL_PASSWORD
    app.config[Params.MYSQL_DATABASE] = MYSQL_DATABASE

    mysql.init_app(app)

    create_tables(app, mysql)

    from ssis.routes.college_bp import college_bp
    from ssis.routes.course_bp import course_bp
    from ssis.routes.main_bp import main_bp
    from ssis.routes.student_bp import student_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/student/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')

    return app
