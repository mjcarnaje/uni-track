import datetime

from flask_login import UserMixin

from ..db import mysql


class University(UserMixin):
    def __init__(self, id: int | None = None, email: str = None, logo: str | None = None, display_name: str = None, name: str = None, primary_color: str = None, secondary_color: str = None, password: str = None, created_at: datetime.datetime | None = None):
        self.id = id
        self.email = email
        self.logo = logo
        self.display_name = display_name
        self.name = name
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.password = password
        self.created_at = created_at

    def get_id(self):
        return self.id

    @classmethod
    def find_by_id(cls, id: int):
        sql = "SELECT * FROM university WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id,))
        university = cur.fetchone()
        if not university:
            return None
        return cls(**university)

    @classmethod
    def find_by_email(cls, email: str):
        sql = "SELECT * FROM university WHERE email=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (email,))
        university = cur.fetchone()
        if not university:
            return None
        return cls(**university)

    @staticmethod
    def insert(email: str, logo: str | None, display_name: str, name: str, primary_color: str, secondary_color: str, password: str):
        sql = "INSERT INTO university (email, logo, display_name, name, primary_color, secondary_color, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, [email, logo, display_name, name, primary_color,
                    secondary_color, password])
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def update(id: int, email: str, logo: str | None, display_name: str, name: str, primary_color: str, secondary_color: str):
        sql = "UPDATE university SET email=%s, logo=%s, display_name=%s, name=%s, primary_color=%s, secondary_color=%s WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (email, logo, display_name, name,
                    primary_color, secondary_color, id))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def delete(id: int):
        sql = "DELETE FROM university WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def check_if_email_exists(email: str, id: int = None):
        sql = "SELECT * FROM university WHERE email=%s"
        params = [email]

        if id:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)

        exists = cur.fetchone() is not None

        return exists
