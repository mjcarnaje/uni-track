CREATE TABLE IF NOT EXISTS university (
    id SERIAL PRIMARY KEY,
    email VARCHAR(256) UNIQUE NOT NULL,
    logo TEXT,
    display_name VARCHAR(256) NOT NULL,
    name VARCHAR(256) NOT NULL,
    primary_color VARCHAR(16) NOT NULL,
    secondary_color VARCHAR(16) NOT NULL,
    password VARCHAR(256) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS college (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    code VARCHAR(16) UNIQUE NOT NULL,
    photo TEXT,
    university_id INTEGER REFERENCES university(id),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS course (
    id SERIAL PRIMARY KEY,
    name VARCHAR(256) UNIQUE NOT NULL,
    code VARCHAR(16) UNIQUE NOT NULL,
    photo TEXT,
    college_id INTEGER REFERENCES college(id),
    university_id INTEGER REFERENCES university(id),
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    student_id VARCHAR(16) UNIQUE NOT NULL,
    first_name VARCHAR(256) NOT NULL,
    last_name VARCHAR(256) NOT NULL,
    gender VARCHAR(16) NOT NULL,
    birthday DATE NOT NULL,
    photo TEXT,
    college_id INTEGER REFERENCES college(id),
    course_id INTEGER REFERENCES course(id),
    university_id INTEGER REFERENCES university(id),
    created_at TIMESTAMP DEFAULT NOW()
);
