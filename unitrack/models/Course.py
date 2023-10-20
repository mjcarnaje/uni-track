from ..db import mysql


class Course():
    __tablename__ = 'course'

    def __init__(self,
                 id: int = None,
                 name: str = None,
                 code: str = None,
                 photo: str = None,
                 college_id: int = None,
                 university_id: int = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo
        self.college_id = college_id
        self.university_id = university_id

    def find_one(self):
        if self.id is None or self.university_id is None:
            raise Exception("Cannot find without an ID and university ID")

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id, self.university_id))
        return cur.fetchone()

    def find_all(self):
        SELECT_SQL = f"SELECT course.*, COUNT(student.id) as student_count FROM {self.__tablename__}"
        SELECT_SQL += " LEFT JOIN student ON student.course_id = course.id GROUP BY course.id"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        return cur.fetchall()

    def find_by_college_id(self, college_id: int):
        if self.university_id is None:
            raise Exception(
                "Cannot find without an university ID")

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE college_id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (college_id, self.university_id))
        return cur.fetchall()

    def insert(self):
        if self.university_id is None:
            raise Exception("Cannot insert without an university ID")

        INSERT_SQL = f"INSERT INTO {self.__tablename__} (name, code, photo, college_id, university_id) VALUES (%s, %s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (self.name, self.code, self.photo,
                    self.college_id, self.university_id))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None:
            raise Exception("Cannot update without an ID")

        UPDATE_SQL = f"UPDATE {self.__tablename__} SET name=%s, code=%s, photo=%s, college_id=%s WHERE id=%s"

        try:
            cur = mysql.new_cursor(dictionary=True)
            cur.execute(
                UPDATE_SQL, (self.name, self.code, self.photo, self.college_id, self.id))

            mysql.connection.commit()

            return "Update successful"
        except Exception as e:
            return f"Update failed: {str(e)}"

    def delete(self):
        if self.id is None or self.university_id is None:
            raise Exception(
                "Cannot delete without an ID and university ID")

        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s AND university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(DELETE_SQL, (self.id, self.university_id))
        mysql.connection.commit()
        return "Delete successful"

    def count(self):
        if self.university_id is None:
            raise Exception(
                "Cannot count without an university ID")

        SELECT_SQL = f"SELECT COUNT(*) FROM {self.__tablename__} WHERE university_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.university_id,))
        return cur.fetchone()['COUNT(*)']

    def check_if_code_exists(self, code: str, id: int = None) -> bool:
        if self.university_id is None:
            raise Exception(
                "Cannot check without an university ID")

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
            raise Exception(
                "Cannot check without an university ID")

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE name=%s AND university_id=%s"
        params = [name, self.university_id]

        if id:
            SELECT_SQL += " AND id != %s"
            params.append(id)

        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, params)
        return cur.fetchone() is not None
