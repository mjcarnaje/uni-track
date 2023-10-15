from ..db import mysql


class College():
    __tablename__ = 'college'

    def __init__(self,
                 name: str = None,
                 code: str = None,
                 photo: str = None,
                 id: int = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo

    def find_one(self) -> str or dict:
        if self.id is None:
            return "Cannot find without an ID"

        SELECT_SQL = f"SELECT college.*, COUNT(course.id) as course_count, COUNT(student.id) as student_count FROM {self.__tablename__} LEFT JOIN course ON course.college_id = college.id LEFT JOIN student ON student.college_id = college.id GROUP BY college.id HAVING college.id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        college = cur.fetchone()
        return college

    def find_all(self, page_number: int = 1, page_size: int = 100, query: str = None):
        offset = (page_number - 1) * page_size

        filter_params = []
        where_clause = ""

        if query:
            where_clause += "name LIKE %s OR code LIKE %s"
            filter_params.append(f"%{query}%")
            filter_params.append(f"%{query}%")

        SELECT_SQL = f"SELECT college.*, COUNT(course.id) as course_count, COUNT(student.id) as student_count FROM {self.__tablename__} LEFT JOIN course ON course.college_id = college.id LEFT JOIN student ON student.college_id = college.id GROUP BY college.id"

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
            'has_next_page': has_next_page,
            'total_count': total_count,
        }

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (name, code, photo) VALUES (%s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (self.name, self.code, self.photo))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None:
            return "Cannot update without an ID"

        UPDATE_SQL = f"UPDATE {self.__tablename__} SET name=%s, code=%s, photo=%s WHERE id=%s"

        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                UPDATE_SQL, (self.name, self.code, self.photo, self.id))

            mysql.connection.commit()

            return "Update successful"
        except Exception as e:
            return f"Update failed: {str(e)}"

    def delete(self):
        if self.id is None:
            return "Cannot delete without an ID"

        try:
            DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s"
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(DELETE_SQL, (self.id,))
            mysql.connection.commit()
            return "Delete successful"
        except Exception as e:
            return f"Delete failed: {str(e)}"

    def find_courses(self):
        if (self.id is None):
            return "Cannot find courses without an ID"

        SELECT_SQL = f"SELECT course.*, COUNT(student.id) as student_count FROM {self.__tablename__} JOIN course ON course.college_id = college.id JOIN student ON student.course_id = course.id WHERE college.id=%s GROUP BY course.id"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        return cur.fetchall()
