from flask import Flask
from flask_login import LoginManager, login_manager
from flask_mysql_connector import MySQL

from .configs import set_configs
from .db import create_tables, mysql
from .models.University import University

app = Flask(__name__)


def create_app():

    set_configs(app)

    mysql.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    create_tables(app=app, mysql=mysql)

    @login_manager.user_loader
    def load_user(user_id):
        return University(id=user_id).find_by_id()

    from unitrack.routes.main_bp import main_bp
    from unitrack.routes.auth_bp import auth_bp
    from unitrack.routes.college_bp import college_bp
    from unitrack.routes.course_bp import course_bp
    from unitrack.routes.student_bp import student_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(student_bp, url_prefix='/student/')

    return app
