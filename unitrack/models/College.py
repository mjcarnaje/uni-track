from ..db import mysql


class College():
    __tablename__ = 'college'

    def __init__(self,
                 name: str = None,
                 code: str = None,
                 photo: str = None,
                 university_id: int = None,
                 id: int = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo
        self.university_id = university_id

    def find_one(self) -> str or dict:
        if self.id is None:
            return "Cannot find without an ID"

        SELECT_SQL = f"SELECT college.*, MAX(course_counts.course_count) as course_count, MAX(student_counts.student_count) as student_count FROM {self.__tablename__}"
        SELECT_SQL += f" LEFT JOIN (SELECT college_id, COUNT(id) AS course_count FROM course GROUP BY college_id) AS course_counts ON course_counts.college_id = college.id"
        SELECT_SQL += f" LEFT JOIN (SELECT college_id, COUNT(id) AS student_count FROM student GROUP BY college_id) AS student_counts ON student_counts.college_id = college.id"
        SELECT_SQL += " WHERE college.id=%s"

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        college = cur.fetchone()
        return college

    def find_all(self, page_number: int = 1, page_size: int = 100, query: str = None) -> dict:
        offset = (page_number - 1) * page_size

        filter_params = []

        where_clause = "college.university_id = %s"
        filter_params.extend([self.university_id])

        if query:
            where_clause += " AND name LIKE %s OR code LIKE %s"
            filter_params.append(f"%{query}%")
            filter_params.append(f"%{query}%")

        SELECT_SQL = f"SELECT college.*, MAX(course_counts.course_count) as course_count, MAX(student_counts.student_count) as student_count FROM {self.__tablename__}"
        SELECT_SQL += f" LEFT JOIN (SELECT college_id, COUNT(id) AS course_count FROM course GROUP BY college_id) AS course_counts ON course_counts.college_id = college.id"
        SELECT_SQL += f" LEFT JOIN (SELECT college_id, COUNT(id) AS student_count FROM student GROUP BY college_id) AS student_counts ON student_counts.college_id = college.id"
        SELECT_SQL += f" WHERE {where_clause}"
        SELECT_SQL += " GROUP BY college.id"
        SELECT_SQL += " LIMIT %s OFFSET %s"

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
            'total_count': total_count,
        }

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (name, code, photo, university_id) VALUES (%s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (self.name, self.code,
                    self.photo, self.university_id))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None or self.university_id is None:
            return "Cannot update without an ID and university ID"

        UPDATE_SQL = f"UPDATE {self.__tablename__} SET name=%s, code=%s, photo=%s WHERE id=%s AND university_id=%s"

        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                UPDATE_SQL, (self.name, self.code, self.photo, self.id, self.university_id))
            mysql.connection.commit()

            return "Update successful"
        except Exception as e:
            return f"Update failed: {str(e)}"

    def delete(self):
        if self.id is None or self.university_id is None:
            return "Cannot delete without an ID and university ID"

        try:
            DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s AND university_id=%s"
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(DELETE_SQL, (self.id, self.university_id))
            mysql.connection.commit()
            return "Delete successful"
        except Exception as e:
            return f"Delete failed: {str(e)}"

    def find_courses(self):
        if (self.id is None or self.university_id is None):
            return "Cannot find courses without an ID and university ID"

        SELECT_SQL = f"SELECT course.*, COUNT(student.id) as student_count FROM {self.__tablename__}"
        SELECT_SQL += " LEFT JOIN course ON course.college_id = college.id"
        SELECT_SQL += " LEFT JOIN student ON student.course_id = course.id"
        SELECT_SQL += " WHERE college.id=%s AND college.university_id=%s"
        SELECT_SQL += " GROUP BY course.id"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id, self.university_id))
        return cur.fetchall()

    def count(self):
        SELECT_SQL = f"SELECT COUNT(*) FROM {self.__tablename__} WHERE university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.university_id,))
        return cur.fetchone()['COUNT(*)']

    def check_if_code_exists(self, code: str, id: int = None) -> bool:
        if self.university_id is None:
            return "Cannot check without an university ID"

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE code=%s AND university_id=%s"
        params = [code, self.university_id]

        if id:
            SELECT_SQL += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, params)
        return cur.fetchone() is not None

    def check_if_name_exists(self, name: str, id: int = None) -> bool:
        if self.university_id is None:
            return "Cannot check without an university ID"

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE name=%s AND university_id=%s"
        params = [name, self.university_id]

        if id:
            SELECT_SQL += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, params)
        return cur.fetchone() is not None
