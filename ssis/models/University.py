from flask_login import UserMixin
from ..db import mysql


class University(UserMixin):
    __tablename__ = 'university'

    def __init__(self, email: str = None, logo: str = None, display_name: str = None, name: str = None, primary_color: str = None, secondary_color: str = None, password: str = None, id: int = None):
        self.id = id
        self.email = email
        self.logo = logo
        self.display_name = display_name
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.password = password

    def get_id(self):
        return self.id

    def find_by_id(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        university = cur.fetchone()
        if not university:
            return False

        self.email = university.get("email")
        self.logo = university.get("logo")
        self.display_name = university.get("display_name")
        self.name = university.get("name")
        self.primary_color = university.get("primary_color")
        self.secondary_color = university.get("secondary_color")
        self.password = university.get("password")

        return self

    def find_by_email(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE email=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.email,))
        university = cur.fetchone()

        if not university:
            return False

        self.id = university.get("id")
        self.logo = university.get("logo")
        self.display_name = university.get("display_name")
        self.name = university.get("name")
        self.primary_color = university.get("primary_color")
        self.secondary_color = university.get("secondary_color")
        self.password = university.get("password")

        return self

    def create(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (email, logo, display_name, name, primary_color, secondary_color, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (
            self.email,
            self.logo,
            self.display_name,
            self.name,
            self.primary_color,
            self.secondary_color,
            self.password
        ))
        mysql.connection.commit()
        self.id = cur.lastrowid
        return self
