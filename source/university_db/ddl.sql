DROP TABLE IF EXISTS teaches;
DROP TABLE IF EXISTS takes;
DROP TABLE IF EXISTS section;
DROP TABLE IF EXISTS prereq; 
DROP TABLE IF EXISTS course;
DROP TABLE IF EXISTS advisor;
DROP TABLE IF EXISTS instructor;
DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS department;


CREATE TABLE department (
    dept_name       VARCHAR(50) PRIMARY KEY, 
    phone           VARCHAR(15), 
    budget          NUMERIC(15, 2) CHECK (budget >= 0),
    building        VARCHAR(50),  
    dean_name       VARCHAR(100)
);

CREATE TABLE student (
    id              INTEGER PRIMARY KEY,  -- SQLite auto-generates ROWID
    fname           VARCHAR(25) NOT NULL, 
    lname           VARCHAR(25) NOT NULL, 
    dept_name       VARCHAR(50) NOT NULL, 
    major           VARCHAR(50), 
    tot_cred        INTEGER CHECK (tot_cred >= 0),  
    email           VARCHAR(60) UNIQUE NOT NULL, 
    enrollment_date DATE DEFAULT CURRENT_DATE,   
    status          VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Inactive', 'Graduated', 'Suspended')),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE RESTRICT ON UPDATE CASCADE 
);

CREATE TABLE instructor (
    id              INTEGER PRIMARY KEY,  -- SQLite auto-generates ROWID
    fname           VARCHAR(25) NOT NULL,
    lname           VARCHAR(25) NOT NULL, 
    dept_name       VARCHAR(50) NOT NULL, 
    academic_rank   VARCHAR(25) CHECK (academic_rank IN ('Assistant Professor', 'Associate Professor', 'Professor', 'Lecturer', 'Adjunct')), 
    salary          NUMERIC(10, 2) CHECK (salary >= 0),  
    email           VARCHAR(60) UNIQUE NOT NULL, 
    hire_date       DATE DEFAULT CURRENT_DATE,
    office_number   VARCHAR(20),
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE advisor (
    student_id      INTEGER,   
    instructor_id   INTEGER, 
    start_date      DATE DEFAULT CURRENT_DATE,  
    end_date        DATE,
    PRIMARY KEY (student_id), 
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE, 
    FOREIGN KEY (instructor_id) REFERENCES instructor(id) ON DELETE SET NULL
); 

CREATE TABLE course (
    course_id       VARCHAR(10) PRIMARY KEY,  -- "CS101A"
    title           VARCHAR(100) NOT NULL,
    credits         INTEGER CHECK (credits > 0 AND credits <= 4) NOT NULL,
    dept_name       VARCHAR(50) NOT NULL,
    description     TEXT,  
    FOREIGN KEY (dept_name) REFERENCES department(dept_name) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE prereq (
    course_id       VARCHAR(10), 
    prereq_id       VARCHAR(10), 
    PRIMARY KEY (course_id, prereq_id), 
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE, 
    FOREIGN KEY (prereq_id) REFERENCES course(course_id) ON DELETE SET NULL
);

CREATE TABLE section (
    course_id       VARCHAR(10), 
    sec_id          VARCHAR(8), 
    semester        VARCHAR(6) CHECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer')),
    academic_year   INTEGER CHECK (academic_year > 1701 AND academic_year < 2100),  
    time_slot       VARCHAR(20),  -- "MWF 10:00-11:00"
    room            VARCHAR(15),
    capacity        INTEGER CHECK (capacity > 0),  -- enrollment capacity
    enrolled        INTEGER DEFAULT 0 CHECK (enrolled >= 0),  -- Current enrollment count
    PRIMARY KEY (course_id, sec_id, semester, academic_year), 
    FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CHECK (enrolled <= capacity)  -- Ensure enrollment doesn't exceed capacity
);

CREATE TABLE takes (
    student_id      INTEGER, 
    course_id       VARCHAR(10), 
    sec_id          VARCHAR(8), 
    semester        VARCHAR(6) CHECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer')),
    academic_year   INTEGER CHECK (academic_year > 1701 AND academic_year < 2100), 
    cancelled       BOOLEAN DEFAULT FALSE, 
    grade           VARCHAR(2) CHECK (grade IN ('A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F')),  -- Letter grades
    enrollment_date DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (student_id, course_id, sec_id, semester, academic_year),
    FOREIGN KEY (student_id) REFERENCES student(id) ON DELETE CASCADE, 
    FOREIGN KEY (course_id, sec_id, semester, academic_year) REFERENCES section ON DELETE CASCADE
);

CREATE TABLE teaches (
    instructor_id   INTEGER, 
    course_id       VARCHAR(10),
    sec_id          VARCHAR(8),  
    semester        VARCHAR(6) CHECK (semester IN ('Fall', 'Winter', 'Spring', 'Summer')),
    academic_year   INTEGER CHECK (academic_year > 1701 AND academic_year < 2100), 
    PRIMARY KEY (instructor_id, course_id, sec_id, semester, academic_year), 
    FOREIGN KEY (instructor_id) REFERENCES instructor(id) ON DELETE CASCADE, 
    FOREIGN KEY (course_id, sec_id, semester, academic_year) REFERENCES section ON DELETE CASCADE
);

/*
-- Create useful indexes for performance
CREATE INDEX idx_student_dept ON student(dept_name);
CREATE INDEX idx_student_email ON student(email);
CREATE INDEX idx_instructor_dept ON instructor(dept_name);
CREATE INDEX idx_course_dept ON course(dept_name);
CREATE INDEX idx_takes_student ON takes(student_id);
CREATE INDEX idx_takes_course ON takes(course_id, semester, academic_year);
CREATE INDEX idx_section_semester ON section(semester, academic_year);
*/;
