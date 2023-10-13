from flask_login import UserMixin
from ..db import mysql


class User(UserMixin):
    __tablename__ = 'user'

    def __init__(self, username: str = None, email: str = None, password: str = None, id: int = None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password

    def get_id(self):
        return self.id

    def find_by_id(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        user = cur.fetchone()

        this_user = User(username=user.get("username"),
                         email=user.get("email"),
                         password=user.get("password"),
                         id=user.get("id"))

        return this_user

    def find_by_username(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE username=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.username,))
        user = cur.fetchone()
        return user

    def find_by_email(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE email=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.email,))
        user = cur.fetchone()

        this_user = User(username=user.get("username"),
                         email=user.get("email"),
                         password=user.get("password"),
                         id=user.get("id"))

        return this_user

    def create(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (username, email, password) VALUES (%s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (self.username, self.email, self.password))
        mysql.connection.commit()
        return cur.lastrowid
