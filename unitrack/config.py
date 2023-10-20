import os


class Config:
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/uploads')

    SECRET_KEY = os.getenv('SECRET_KEY')

    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_USER = os.getenv('MYSQL_USER')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
