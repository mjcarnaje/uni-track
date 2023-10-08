-- Create the College table with id as STRING
CREATE TABLE college (
    id VARCHAR(16) PRIMARY KEY,
    name VARCHAR(256) UNIQUE,
    code VARCHAR(16) UNIQUE,
    photo TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the Course table with id as STRING
CREATE TABLE course (
    id VARCHAR(16) PRIMARY KEY,
    name VARCHAR(256) UNIQUE,
    code VARCHAR(16) UNIQUE,
    photo TEXT,
    college_id VARCHAR(16) REFERENCES college(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create the Gender enumeration type
CREATE TYPE gender AS ENUM ('Male', 'Female', 'Other');

-- Create the Student table with id as STRING
CREATE TABLE student (
    id VARCHAR(16) PRIMARY KEY,
    student_id VARCHAR(16) UNIQUE,
    first_name VARCHAR(256),
    last_name VARCHAR(256),
    gender gender,
    birthday DATE,
    photo TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    college_id VARCHAR(16) REFERENCES college(id),
    course_id VARCHAR(16) REFERENCES course(id)
);
