from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from unitrack.config import Config

from .db import mysql
from .db.create_tables import create_tables
from .models.University import University
import cloudinary
from cloudinary.utils import cloudinary_url


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    CSRFProtect(app)

    cloudinary.config(cloud_name=Config.CLOUDINARY_CLOUD_NAME,
                      api_key=Config.CLOUDINARY_API_KEY,
                      api_secret=Config.CLOUDINARY_API_SECRET,
                      )

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    create_tables(app)

    @login_manager.user_loader
    def load_user(user_id):
        return University.find_by_id(user_id)

    @app.context_processor
    def utility_processor():
        def get_image(public_id):
            source = public_id if public_id else f"{Config.CLOUDINARY_FOLDER}/default"
            url, options = cloudinary_url(public_id, format="jpg", crop="fill")
            return url
        return dict(get_image=get_image)

    from unitrack.routes.auth_bp import auth_bp
    from unitrack.routes.college_bp import college_bp
    from unitrack.routes.course_bp import course_bp
    from unitrack.routes.main_bp import main_bp
    from unitrack.routes.student_bp import student_bp

    app.register_blueprint(main_bp, url_prefix='/')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(college_bp, url_prefix='/college/')
    app.register_blueprint(course_bp, url_prefix='/course/')
    app.register_blueprint(student_bp, url_prefix='/student/')

    return app
