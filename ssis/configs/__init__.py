from flask_mysql_connector import Params
from flask import Flask

UPLOAD_FOLDER = 'ssis/static/uploads'
SECRET_KEY = 'this-is-a-secret-key'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'ssis'


def set_configs(app: Flask):
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config[Params.MYSQL_HOST] = MYSQL_HOST
    app.config[Params.MYSQL_USER] = MYSQL_USER
    app.config[Params.MYSQL_PASSWORD] = MYSQL_PASSWORD
    app.config[Params.MYSQL_DATABASE] = MYSQL_DATABASE
