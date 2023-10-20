from flask import Flask
import os
from ..db import mysql

script_path = os.path.join(os.path.dirname(
    __file__), 'create_tables_script.sql')


def create_tables(app: Flask):
    with open(script_path, 'r') as f:
        sql = f.read()
        with app.app_context():
            sql = sql.split(';')
            sql.pop()
            cur = mysql.connection.cursor()
            for statement in sql:
                cur.execute(statement)
                mysql.connection.commit()
