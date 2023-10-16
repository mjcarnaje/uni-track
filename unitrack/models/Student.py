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
                 student_id: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 gender: Gender = None,
                 birthday: datetime.datetime = None,
                 photo: str = None,
                 college_id: int = None,
                 course_id: int = None,
                 university_id: int = None,
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
        self.university_id = university_id

    def find_one(self):
        if self.id is None and self.university_id is None:
            return "Cannot find without an ID and university ID"

        SELECT_SQL = f"SELECT student.*, college.name AS college_name, college.photo AS college_photo, course.name AS course_name, course.photo AS course_photo FROM {self.__tablename__}"
        SELECT_SQL += " LEFT JOIN college ON student.college_id = college.id JOIN course ON student.course_id = course.id WHERE student.id=%s AND student.university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id, self.university_id))
        student = cur.fetchone()
        return student

    def find_all(self, page_number: int, page_size: int, query: str, college_id: str, course_id: str, gender: str) -> dict:
        offset = (page_number - 1) * page_size

        filter_params = []

        where_clause = "student.university_id = %s"
        filter_params.extend([self.university_id])

        if query:
            where_clause += " AND student_id LIKE %s OR first_name LIKE %s OR last_name LIKE %s"
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

        SELECT_SQL = f"SELECT student.*, college.name AS college_name, college.photo AS college_photo, course.name AS course_name, course.photo AS course_photo FROM {self.__tablename__}"
        SELECT_SQL += " JOIN college ON student.college_id = college.id JOIN course ON student.course_id = course.id"
        SELECT_SQL += f" WHERE {where_clause}"
        SELECT_SQL += " LIMIT %s OFFSET %s"

        print(f"SELECT SQL: {SELECT_SQL}")

        for i in filter_params + [page_size, offset]:
            print(i)

        cur = mysql.new_cursor(dictionary=True)

        cur.execute(SELECT_SQL, filter_params + [page_size, offset])

        data = cur.fetchall()

        COUNT_SQL = f"SELECT COUNT(*) FROM {self.__tablename__}"
        COUNT_SQL += f" WHERE {where_clause}"

        cur.execute(COUNT_SQL, filter_params)
        total_count = cur.fetchone()['COUNT(*)']

        has_previous_page = offset > 0
        has_next_page = (offset + page_size) < total_count

        return {
            'data': data,
            'has_previous_page': has_previous_page,
            'has_next_page': has_next_page,
            'total_count': total_count
        }

    def insert(self) -> str:
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (student_id, first_name, last_name, gender, birthday, photo, college_id, course_id, university_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (self.student_id, self.first_name, self.last_name, self.gender,
                    self.birthday, self.photo, self.college_id, self.course_id, self.university_id))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None or self.university_id is None:
            return "Cannot update without an ID and university ID"

        UPDATE_SQL = f"UPDATE {self.__tablename__} SET student_id=%s, first_name=%s, last_name=%s, gender=%s, birthday=%s, photo=%s, college_id=%s, course_id=%s WHERE id=%s"

        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(UPDATE_SQL, (self.student_id, self.first_name, self.last_name,
                        self.gender, self.birthday, self.photo, self.college_id, self.course_id, self.id))
            mysql.connection.commit()
            return "Update successful"
        except Exception as e:
            return f"Update failed: {str(e)}"

    def delete(self):
        if self.id is None or self.university_id is None:
            return "Cannot delete without an ID and university ID"

        try:
            DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s"
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(DELETE_SQL, (self.id,))
            mysql.connection.commit()
        except Exception as e:
            return f"Delete failed: {str(e)}"

        return "Delete successful"
