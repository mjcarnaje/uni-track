from flask import Flask
from flask_mysql_connector import MySQL

from .configs import set_configs
from .db import create_tables

mysql = MySQL()


def create_app():
    app = Flask(__name__)

    set_configs(app)

    mysql.init_app(app)

    create_tables(app=app, mysql=mysql)

    from ssis.routes.college_bp import college_bp
    from ssis.routes.course_bp import course_bp
    from ssis.routes.main_bp import main_bp
    from ssis.routes.student_bp import student_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(student_bp, url_prefix='/student/')

    return app
