CREATE TABLE IF NOT EXISTS college (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    code VARCHAR(16) UNIQUE NOT NULL,
    photo TEXT
);
CREATE TABLE IF NOT EXISTS course (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    code VARCHAR(16) UNIQUE NOT NULL,
    photo TEXT,
    college_id INTEGER REFERENCES college(id)
);
CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(16) UNIQUE NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    birthday DATE NOT NULL,
    photo TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    college_id INTEGER REFERENCES college(id),
    course_id INTEGER REFERENCES course(id)
);