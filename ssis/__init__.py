from flask import Flask
from flask_mysql_connector import MySQL


UPLOAD_FOLDER = 'ssis/static/uploads'
SECRET_KEY = 'this-is-a-secret-key'
mysql = MySQL()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'password'
    app.config['MYSQL_DATABASE'] = 'ssis'

    mysql.init_app(app)

    # from ssis.routes.auth_bp import auth_bp
    from ssis.routes.college_bp import college_bp
    from ssis.routes.student_bp import student_bp
    from ssis.routes.main_bp import main_bp
    from ssis.routes.course_bp import course_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(student_bp, url_prefix='/student/')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    # app.register_blueprint(auth_bp, url_prefix='/auth/')

    return app
