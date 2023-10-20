import datetime
from ..db import mysql


class Course():
    def __init__(self,
                 id: int = None,
                 name: str = None,
                 code: str = None,
                 photo: str | None = None,
                 college_id: int = None,
                 university_id: int = None,
                 created_at: datetime.datetime | None = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo
        self.college_id = college_id
        self.university_id = university_id
        self.created_at = created_at

    @classmethod
    def find_by_id(cls, university_id: int, id: int):
        sql = f"SELECT * FROM course WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id))
        course = cur.fetchone()
        if not course:
            return None
        return cls(**course)

    @staticmethod
    def find_by_college_id(university_id: int, college_id: int):
        sql = """
        SELECT course.*, COUNT(student.id) AS student_count
        FROM course
        LEFT JOIN student ON course.id = student.course_id
        WHERE course.college_id = %s AND course.university_id = %s
        GROUP BY course.id;
        """
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (college_id, university_id))
        return cur.fetchall()

    @staticmethod
    def insert(name: str, code: str, photo: str | None, college_id: int, university_id: int):
        sql = f"INSERT INTO course (name, code, photo, college_id, university_id) VALUES (%s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (name, code, photo, college_id, university_id))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def update(id: int, name: str, code: str, photo: str | None, college_id: int, university_id: int):
        sql = "UPDATE course SET name=%s, code=%s, photo=%s, college_id=%s WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (name, code, photo, college_id,
                    id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def delete(id: int, university_id: int):
        sql = "DELETE FROM course WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def count(university_id: int):
        sql = "SELECT COUNT(*) FROM course WHERE university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (university_id,))
        return int(cur.fetchone()['COUNT(*)'])

    @staticmethod
    def check_if_code_exists(code: str, university_id: int, id: int = None) -> bool:
        sql = "SELECT * FROM course WHERE code=%s AND university_id=%s"
        params = [code, university_id]

        if id is not None:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone() is not None

    @staticmethod
    def check_if_name_exists(name: str, university_id: int, id: int = None) -> bool:
        sql = "SELECT * FROM course WHERE name=%s AND university_id=%s"
        params = [name, university_id]

        if id is not None:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone() is not None
