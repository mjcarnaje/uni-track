from flask import Flask, jsonify, redirect, request, send_from_directory, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from unitrack.config import Config

from .db import mysql
from .db.create_tables import create_tables
from .db.seed import seed
from .models.University import University
from .utils.upload_file import upload_file


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mysql.init_app(app)
    CSRFProtect(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    create_tables(app)

    @login_manager.user_loader
    def load_user(user_id):
        return University.find_by_id(user_id)

    @app.route('/upload', methods=['POST'])
    def upload():
        return jsonify({'url': upload_file('upload')})

    @app.route('/upload/<path:filename>')
    def media(filename):
        pathlike = filename or 'default.png'
        return send_from_directory(Config.UPLOAD_FOLDER, pathlike, as_attachment=True)

    @app.route('/seed', methods=['POST', 'GET'])
    def seed_database():
        if request.method == 'POST':
            seed()
            return redirect('/')
        return render_template('seed_database.html')

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
