from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Config:
    UPLOAD_FOLDER = 'unitrack/static/uploads'
    SECRET_KEY = getenv('SECRET_KEY')

    MYSQL_HOST = getenv('MYSQL_HOST')
    MYSQL_USER = getenv('MYSQL_USER')
    MYSQL_PASSWORD = getenv('MYSQL_PASSWORD')
    MYSQL_DATABASE = getenv('MYSQL_DATABASE')
