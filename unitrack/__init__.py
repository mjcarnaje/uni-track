from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from .db import create_tables, mysql
from .models.University import University
from unitrack.config import Config

app = Flask(__name__)


def create_app():

    app.config.from_object(Config)

    mysql.init_app(app)
    CSRFProtect(app)

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
