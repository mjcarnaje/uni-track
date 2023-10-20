import datetime

from ..db import mysql


class College():
    def __init__(self,
                 id: int = None,
                 name: str = None,
                 code: str = None,
                 photo: str | None = None,
                 university_id: int = None,
                 created_at: datetime.datetime | None = None,
                 course_count: int | None = None,
                 student_count: int | None = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo
        self.university_id = university_id
        self.created_at = created_at
        self.course_count = course_count
        self.student_count = student_count

    @classmethod
    def find_by_id(cls, university_id: int, id: int):
        sql = """SELECT 
                    college.*, 
                    (SELECT COUNT(id) FROM course WHERE college_id = college.id) AS course_count,
                    (SELECT COUNT(id) FROM student WHERE college_id = college.id) AS student_count
                FROM college
                WHERE college.id=%s AND college.university_id=%s"""

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id))
        college = cur.fetchone()
        if not college:
            return None
        return cls(**college)

    @staticmethod
    def find_all(university_id: int, page_number: int = 1, page_size: int = 100, query: str = None):
        offset = (page_number - 1) * page_size

        where_clause = "college.university_id = %s"
        filter_params = [university_id]

        if query:
            where_clause += " AND name LIKE %s OR code LIKE %s"
            filter_params.append(f"%{query}%")
            filter_params.append(f"%{query}%")

        sql = """SELECT 
                    college.*, 
                    (SELECT COUNT(id) FROM course WHERE college_id = college.id) AS course_count,
                    (SELECT COUNT(id) FROM student WHERE college_id = college.id) AS student_count
                FROM college"""
        sql += f" WHERE {where_clause}"
        sql += " GROUP BY college.id"
        sql += " LIMIT %s OFFSET %s"

        cur = mysql.new_cursor(dictionary=True)

        cur.execute(sql, filter_params + [page_size, offset])

        data = cur.fetchall()

        count_sql = f"SELECT COUNT(*) FROM college"
        count_sql += f" WHERE {where_clause}"

        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['COUNT(*)']

        has_previous_page = offset > 0
        has_next_page = (offset + page_size) < total_count

        return {
            'data': data,
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page,
            'total_count': total_count,
        }

    @staticmethod
    def insert(name: str, code: str, photo: str | None, university_id: int):
        sql = "INSERT INTO college (name, code, photo, university_id) VALUES (%s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (name, code, photo, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def update(id: int, name: str, code: str, photo: str | None, university_id: int):
        sql = "UPDATE college SET name=%s, code=%s, photo=%s WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (name, code, photo, id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def delete(id: int, university_id: int):
        sql = "DELETE FROM college WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def count(university_id: int):
        sql = "SELECT COUNT(*) FROM college WHERE university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (university_id,))
        return cur.fetchone()['COUNT(*)']

    @staticmethod
    def check_if_code_exists(code: str, university_id: int, id: int = None) -> bool:
        sql = "SELECT * FROM college WHERE code=%s AND university_id=%s"
        params = [code, university_id]

        if id is not None:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone() is not None

    @staticmethod
    def check_if_name_exists(name: str, university_id: int, id: int = None) -> bool:
        sql = "SELECT * FROM college WHERE name=%s AND university_id=%s"
        params = [name, university_id]

        if id is not None:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone() is not None
