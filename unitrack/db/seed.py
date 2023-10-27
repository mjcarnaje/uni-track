import random
from werkzeug.security import generate_password_hash
from . import mysql

universities = [
    {
        'id': 1,
        'email': 'msuiit@gmail.com',
        'logo': '51411590-9e62-44ef-9890-0136d38582f6.png',
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
        'photo': 'ea216607-39a4-47f2-bea5-9ffc4510e1c6.jpg',
        'university_id': 1,
    },
    {
        'id': 2,
        'name': 'College of Arts and Social Sciences',
        'code': 'CASS',
        'photo': 'ff8b44d7-dc78-4bde-b243-3668a8126463.jpg',
        'university_id': 1,
    },
    {
        'id': 3,
        'name': 'College of Science and Mathematics',
        'code': 'CSM',
        'photo': '48e3aac3-b70c-4b03-9cae-66729509b775.jpg',
        'university_id': 1,
    },
    {
        'id': 4,
        'name': 'College of Computer Studies',
        'code': 'CASS',
        'photo': '5951c591-efb3-44b0-b8b7-41e75c7bdbdd.jpg',
        'university_id': 2,
    }
]

courses = [
    {
        'id': 1,
        'name': 'Bachelor of Science in Computer Science',
        'code': 'BSCS',
        'photo': 'adf5d536-a771-4e60-8c93-e2e4207504bb.png',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 2,
        'name': 'Bachelor of Science in Information Technology',
        'code': 'BSIT',
        'photo': 'cd043674-9062-48dd-ba80-23e1f7502444.jpg',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 3,
        'name': 'Bachelor of Science in Information Systems',
        'code': 'BSIS',
        'photo': 'ef2173fe-71a3-4d95-ad91-7dbcd32caad5.jpg',
        'college_id': 1,
        'university_id': 1,
    },
    {
        'id': 4,
        'name': 'Bachelor of Science in Psychology',
        'code': 'BSPsych',
        'photo': 'd435479d-f1d4-4095-a3e1-8c5341a5b462.jpg',
        'college_id': 2,
        'university_id': 1,
    },
    {
        'id': 5,
        'name': 'Bachelor of Science in Political Science',
        'code': 'BSPolSci',
        'photo': '8246bc0d-004e-4b78-ad69-ba1ba9f49c58.jpg',
        'college_id': 2,
        'university_id': 1,
    },
    {
        'id': 6,
        'name': 'Bachelor of Science in Statistics',
        'code': 'BSStats',
        'photo': '711d3cfc-1f53-4bd1-8a96-111d45f19c6b.jpg',
        'college_id': 3,
        'university_id': 1,
    },
    {
        'id': 7,
        'name': 'Bachelor of Science in Mathematics',
        'code': 'BSMath',
        'photo': 'b66aad32-686f-48c6-ac86-9c078082b1c4.jpg',
        'college_id': 3,
        'university_id': 1,
    },
    {
        'id': 8,
        'name': 'Bachelor of Science in Psychology',
        'code': 'BSPsych',
        'photo': 'b402cee9-7735-43a4-a90f-8d53c1d1315c.jpg',
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
        photo = "1b43b702-c8e8-464c-898f-0ee46dbc81ac.png"
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
