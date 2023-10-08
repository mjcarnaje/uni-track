import enum
import datetime

from .. import mysql


class Gender(enum.Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class Student():
    __tablename__ = 'student'

    def __init__(self,
                 student_id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 gender: Gender = None,
                 birthday: datetime.datetime = None,
                 photo: str = None,
                 college_id: int = None,
                 course_id: int = None,
                 created_at: datetime.datetime = None,
                 id: int = None
                 ):
        self.id = id
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.photo = photo
        self.college_id = college_id
        self.course_id = course_id
        self.created_at = created_at

    def find_one(self):
        if self.id is None:
            return "Cannot find without an ID"

        SELECT_SQL = f"SELECT student.*, college.id AS college_id, college.name AS name, course.id AS course_id, course.name AS course_name FROM {self.__tablename__} JOIN college ON student.college_id = college.id JOIN course ON student.course_id = course.id WHERE student.id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        student = cur.fetchone()
        print(student)
        return {
            'id': student.get('id'),
            'student_id': student.get('student_id'),
            'first_name': student.get('first_name'),
            'last_name': student.get('last_name'),
            'gender': student.get('gender'),
            'birthday': student.get('birthday').strftime("%Y-%m-%d"),
            'photo': student.get('photo') or 'default.png',
            'created_at': student.get('created_at').strftime("%Y-%m-%d %H:%M:%S"),
            'college': {
                'id': student.get('college_id'),
                'name': student.get('name'),
            },
            'course': {
                'id': student.get('course_id'),
                'name': student.get('course_name'),
            },

        }

    def find_all(self, page_number: int, page_size: int, query: str, college_id: str, course_id: str):
        offset = (page_number - 1) * page_size

        sql_filter = []
        filter_params = []

        if query:
            sql_filter.append("first_name LIKE %s")
            filter_params.append(f"%{query}%")

        if college_id:
            sql_filter.append("college_id = %s")
            filter_params.append(college_id)

        if course_id:
            sql_filter.append("course_id = %s")
            filter_params.append(course_id)

        where_clause = " AND ".join(sql_filter) if sql_filter else ""

        SELECT_SQL = f"SELECT * FROM {self.__tablename__}"

        if where_clause:
            SELECT_SQL += f" WHERE {where_clause}"

        SELECT_SQL += " LIMIT %s OFFSET %s"
        params = filter_params + [page_size, offset]

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, params)

        data = cur.fetchall()

        COUNT_SQL = f"SELECT COUNT(*) FROM {self.__tablename__}"

        if where_clause:
            COUNT_SQL += f" WHERE {where_clause}"

        cur.execute(COUNT_SQL, filter_params)
        total_count = cur.fetchone()['COUNT(*)']

        has_previous_page = offset > 0
        has_next_page = (offset + page_size) < total_count

        return {
            'data': data,
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page
        }

    def insert(self) -> str:
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (student_id, first_name, last_name, gender, birthday, photo, college_id, course_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (
            self.student_id,
            self.first_name,
            self.last_name,
            self.gender,
            self.birthday,
            self.photo,
            self.college_id,
            self.course_id,
        ))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None:
            return "Cannot update without an ID"

        UPDATE_SQL = f"UPDATE {self.__tablename__} SET student_id=%s, first_name=%s, last_name=%s, gender=%s, birthday=%s, photo=%s, college_id=%s, course_id=%s WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(UPDATE_SQL, (
            self.student_id,
            self.first_name,
            self.last_name,
            self.gender,
            self.birthday,
            self.photo,
            self.college_id,
            self.course_id,
            self.id
        ))
        mysql.connection.commit()
        return "Update successful"

    def delete(self):
        if self.id is None:
            return "Cannot delete without an ID"

        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(DELETE_SQL, (self.id,))
        mysql.connection.commit()
        return "Delete successful"
