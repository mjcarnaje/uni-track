from flask_mysql_connector import Params
from flask import Flask

UPLOAD_FOLDER = 'unitrack/static/uploads'
SECRET_KEY = '628c6f1857f275d393e6b9657fd5e640472239f4d30d72fdf323d43ea3437abf'

MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'password'
MYSQL_DATABASE = 'unitrack'


def set_configs(app: Flask):
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.config[Params.MYSQL_HOST] = MYSQL_HOST
    app.config[Params.MYSQL_USER] = MYSQL_USER
    app.config[Params.MYSQL_PASSWORD] = MYSQL_PASSWORD
    app.config[Params.MYSQL_DATABASE] = MYSQL_DATABASE
