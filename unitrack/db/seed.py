import random
from werkzeug.security import generate_password_hash
from . import mysql

universities = [
    {
        'id': 1,
        'email': 'msuiit@gmail.com',
        'logo': 'unitrack/msu-iit',
        'display_name': 'MSU-IIT',
        'name': 'Mindanao State University - Iligan Institute of Technology',
        'primary_color': '#cc0000',
        'secondary_color': '#ffcc00',
        'password': generate_password_hash('password')
    }
]

colleges = [
    {
        'id': 1,
        'name': 'College of Computer Studies',
        'code': 'CCS',
        'photo': 'unitrack/ccs',
        'university_id': 1,
    },
    {
        'id': 2,
        'name': 'College of Arts and Social Sciences',
        'code': 'CASS',
        'photo': 'unitrack/cass',
        'university_id': 1,
    },
    {
        'id': 3,
        'name': 'College of Science and Mathematics',
        'code': 'CSM',
        'photo': 'unitrack/csm',
        'university_id': 1,
    }
]

courses = [
    {
        'id': 1,
        'name': 'Bachelor of Science in Computer Science',
        'code': 'BSCS',
        'photo': 'unitrack/ccs',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 2,
        'name': 'Bachelor of Science in Information Technology',
        'code': 'BSIT',
        'photo': 'unitrack/ccs',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 3,
        'name': 'Bachelor of Science in Information Systems',
        'code': 'BSIS',
        'photo': 'unitrack/ccs',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 4,
        'name': 'Bachelor of Science in Psychology',
        'code': 'BSPsych',
        'photo': 'unitrack/cass',
        'college_id': 2,
        'university_id': 1,
    },
    {
        'id': 5,
        'name': 'Bachelor of Science in Political Science',
        'code': 'BSPolSci',
        'photo': 'unitrack/cass',
        'college_id': 2,
        'university_id': 1,
    },
    {
        'id': 6,
        'name': 'Bachelor of Science in Statistics',
        'code': 'BSStats',
        'photo': 'unitrack/csm',
        'college_id': 3,
        'university_id': 1,
    },
    {
        'id': 7,
        'name': 'Bachelor of Science in Mathematics',
        'code': 'BSMath',
        'photo': 'unitrack/csm',
        'college_id': 3,
        'university_id': 1,
    },
    {
        'id': 8,
        'name': 'Bachelor of Science in Psychology',
        'code': 'BSPsych',
        'photo': 'unitrack/cass',
        'college_id': 4,
        'university_id': 2,
    }
]


def insert_university():
    sql_statements = []
    for university in universities:
        sql = "INSERT INTO university (email, logo, display_name, name, primary_color, secondary_color, password)"
        sql += " VALUES (%s, %s, %s, %s, %s, %s, %s);"
        values = (university['email'], university['logo'], university['display_name'], university['name'],
                  university['primary_color'], university['secondary_color'], university['password'])
        sql_statements.append((sql, values))
    return sql_statements


def insert_colleges():
    sql_statements = []
    for college in colleges:
        sql = "INSERT INTO college (name, code, photo, university_id)"
        sql += " VALUES (%s, %s, %s, %s);"
        values = (college['name'], college['code'],
                  college['photo'], college['university_id'])
        sql_statements.append((sql, values))
    return sql_statements


def insert_courses():
    sql_statements = []
    for course in courses:
        sql = "INSERT INTO course (name, code, photo, college_id, university_id)"
        sql += " VALUES (%s, %s, %s, %s, %s);"
        values = (course['name'], course['code'], course['photo'],
                  course['college_id'], course['university_id'])
        sql_statements.append((sql, values))
    return sql_statements


def insert_students():
    sql_statements = []
    for _ in range(50):
        first_name = 'First ' + str(random.randint(1, 50))
        last_name = 'Last ' + str(random.randint(51, 100))
        gender = random.choice(['Male', 'Female'])
        birthday = f'19{random.randint(60, 99)}-{random.randint(1, 12)}-{random.randint(1, 28)}'
        photo = "unitrack/default"
        year_enrolled = random.randint(2010, 2023)
        student_id = f'{year_enrolled}-{random.randint(1000, 9999)}'
        college_id = random.choice([1, 2, 3, 4])
        course_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8])
        university_id = random.choice([1])
        values = (student_id, first_name, last_name, gender, birthday,
                  photo, year_enrolled, college_id, course_id, university_id)
        sql = "INSERT INTO student (student_id, first_name, last_name, gender, birthday, photo, year_enrolled, college_id, course_id, university_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        sql_statements.append((sql, values))
    return sql_statements


def seed():
    sql_statements = []
    sql_statements.extend(insert_university())
    sql_statements.extend(insert_colleges())
    sql_statements.extend(insert_courses())
    sql_statements.extend(insert_students())

    with mysql.connection.cursor() as cursor:
        print('Seeding database...')
        for sql, values in sql_statements:
            print(sql, values)
            cursor.execute(sql, values)
        mysql.connection.commit()
