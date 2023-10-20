import datetime
import enum

from ..db import mysql


class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class Student():
    __tablename__ = 'student'

    def __init__(self,
                 id: int | None = None,
                 student_id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 gender: Gender = None,
                 birthday: datetime.datetime = None,
                 photo: str | None = None,
                 year_enrolled: int = None,
                 college_id: int = None,
                 course_id: int = None,
                 university_id: int = None,
                 created_at: datetime.datetime | None = None,
                 college_name: str = None,
                 college_photo: str = None,
                 course_name: str = None,
                 course_photo: str = None
                 ):
        self.id = id
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.photo = photo
        self.college_id = college_id
        self.year_enrolled = year_enrolled
        self.course_id = course_id
        self.university_id = university_id
        self.created_at = created_at
        self.college_name = college_name
        self.college_photo = college_photo
        self.course_name = course_name
        self.course_photo = course_photo

    @classmethod
    def find_by_id(cls, id: int, university_id: int):
        sql = """
            SELECT student.*, college.name AS college_name, college.photo AS college_photo, course.name AS course_name, course.photo AS course_photo FROM student
            LEFT JOIN college ON student.college_id = college.id JOIN course ON student.course_id = course.id 
            WHERE student.id=%s AND student.university_id=%s"""
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id))
        student = cur.fetchone()
        if not student:
            return None
        return cls(**student)

    @staticmethod
    def find_all(university_id: int, page_number: int, page_size: int, query: str, college_id: int, course_id: int, gender: str, year_enrolled: int):
        offset = (page_number - 1) * page_size

        where_clause = "student.university_id = %s"
        filter_params = [university_id]

        if query:
            where_clause += " AND (student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s)"
            filter_params.append(f"%{query}%")
            filter_params.append(f"%{query}%")
            filter_params.append(f"%{query}%")

        if college_id:
            where_clause += " AND student.college_id = %s"
            filter_params.append(college_id)

        if course_id:
            where_clause += " AND student.course_id = %s"
            filter_params.append(course_id)

        if gender:
            where_clause += " AND gender = %s"
            filter_params.append(gender)

        if year_enrolled:
            where_clause += " AND year_enrolled = %s"
            filter_params.append(year_enrolled)

        sql = f"""
                SELECT student.*, college.code AS college_code, college.photo AS college_photo, course.code AS course_code, course.photo AS course_photo FROM student
                JOIN college ON student.college_id = college.id JOIN course ON student.course_id = course.id"""
        sql += f" WHERE {where_clause}"
        sql += " LIMIT %s OFFSET %s"

        print(sql)

        cur = mysql.new_cursor(dictionary=True)

        cur.execute(sql, filter_params + [page_size, offset])

        data = cur.fetchall()

        count_sql = f"SELECT COUNT(*) FROM student"
        count_sql += f" WHERE {where_clause}"

        cur.execute(count_sql, filter_params)
        total_count = cur.fetchone()['COUNT(*)']

        has_previous_page = offset > 0
        has_next_page = (offset + page_size) < total_count

        return {
            'data': data,
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page,
            'total_count': total_count
        }

    @staticmethod
    def insert(student_id: str, first_name: str, last_name: str, gender: str, birthday: datetime.datetime, photo: str, year_enrolled: int, college_id: int, course_id: int, university_id: int) -> str:
        sql = "INSERT INTO student (student_id, first_name, last_name, gender, birthday, photo, year_enrolled, college_id, course_id, university_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (student_id, first_name, last_name, gender,
                    birthday, photo, year_enrolled, college_id, course_id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def update(id: int, student_id: str, first_name: str, last_name: str, gender: str, birthday: datetime.datetime, photo: str, year_enrolled: int, college_id: int, course_id: int, university_id: int) -> str:
        sql = "UPDATE student SET student_id=%s, first_name=%s, last_name=%s, gender=%s, birthday=%s, photo=%s, year_enrolled=%s, college_id=%s, course_id=%s WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (student_id, first_name, last_name, gender,
                    birthday, photo, year_enrolled, college_id, course_id, id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def delete(id: int, university_id: int) -> str:
        sql = "DELETE FROM student WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (id, university_id,))
        mysql.connection.commit()
        return cur.lastrowid

    @staticmethod
    def count(university_id: int):
        sql = "SELECT COUNT(*) FROM student WHERE university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, (university_id,))
        return cur.fetchone()['COUNT(*)']

    @staticmethod
    def check_if_student_id_exists(student_id: str, university_id: int, id: int = None):
        sql = "SELECT * FROM student WHERE university_id=%s AND student_id=%s"
        params = [university_id, student_id]

        if id is not None:
            sql += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(sql, params)
        return cur.fetchone() is not None
