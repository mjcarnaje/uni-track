from ..db import mysql


class Course():
    __tablename__ = 'course'

    def __init__(self,
                 id: int = None,
                 name: str = None,

                 code: str = None,
                 photo: str = None,
                 college_id: int = None
                 ):
        self.id = id
        self.name = name
        self.code = code
        self.photo = photo
        self.college_id = college_id

    def find_one(self):
        if self.id is None:
            return "Cannot find without an ID"

        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (self.id,))
        return cur.fetchone()

    def find_all(self):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__}"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL)
        return cur.fetchall()

    def find_by_college_id(self, college_id: int):
        SELECT_SQL = f"SELECT * FROM {self.__tablename__} WHERE college_id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(SELECT_SQL, (college_id,))
        return cur.fetchall()

    def insert(self):
        INSERT_SQL = f"INSERT INTO {self.__tablename__} (name, code, photo, college_id) VALUES (%s, %s, %s, %s)"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(INSERT_SQL, (
            self.name,
            self.code,
            self.photo,
            self.college_id
        ))
        mysql.connection.commit()
        return "Insert successful"

    def update(self):
        if self.id is None:
            return "Cannot update without an ID"

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
        if self.id is None:
            return "Cannot delete without an ID"

        DELETE_SQL = f"DELETE FROM {self.__tablename__} WHERE id=%s"
        cur = mysql.new_cursor(dictionary=True)
        cur.execute(DELETE_SQL, (id,))
        mysql.connection.commit()
        return "Delete successful"
