-- University Database Population Script
-- Updated for schema with separate prereq table


DELETE FROM advisor;
DELETE FROM takes;
DELETE FROM teaches;
DELETE FROM section;
DELETE FROM prereq;
DELETE FROM course;
DELETE FROM student;
DELETE FROM instructor;
DELETE FROM department;


-- Populate Departments
INSERT INTO department (dept_name, phone, budget, building, dean_name) VALUES
('Computer Science', '555-0101', 2500000.00, 'Engineering Building', 'Dr. Sarah Chen'),
('Mathematics', '555-0102', 1800000.00, 'Science Hall', 'Dr. Michael Rodriguez'),
('Physics', '555-0103', 3200000.00, 'Physics Complex', 'Dr. Jennifer Williams'),
('English', '555-0104', 1200000.00, 'Humanities Building', 'Dr. Robert Johnson'),
('Business Administration', '555-0105', 2800000.00, 'Business School', 'Dr. Lisa Anderson'),
('Biology', '555-0106', 2100000.00, 'Life Sciences Building', 'Dr. David Park'),
('Psychology', '555-0107', 1500000.00, 'Social Sciences Hall', 'Dr. Maria Garcia');

-- Populate Instructors (without specifying id - auto-generated)
INSERT INTO instructor (fname, lname, dept_name, academic_rank, salary, email, hire_date, office_number) VALUES
('John', 'Smith', 'Computer Science', 'Professor', 95000.00, 'j.smith@university.edu', '2010-08-15', 'ENG-301'),
('Emily', 'Davis', 'Computer Science', 'Associate Professor', 75000.00, 'e.davis@university.edu', '2015-01-20', 'ENG-305'),
('Michael', 'Brown', 'Mathematics', 'Professor', 88000.00, 'm.brown@university.edu', '2008-09-01', 'SCI-201'),
('Sarah', 'Wilson', 'Physics', 'Assistant Professor', 65000.00, 's.wilson@university.edu', '2020-08-15', 'PHY-102'),
('Robert', 'Taylor', 'English', 'Professor', 78000.00, 'r.taylor@university.edu', '2005-01-10', 'HUM-250'),
('Jessica', 'Martinez', 'Business Administration', 'Associate Professor', 82000.00, 'j.martinez@university.edu', '2016-08-20', 'BUS-410'),
('David', 'Lee', 'Biology', 'Assistant Professor', 68000.00, 'd.lee@university.edu', '2019-01-15', 'LS-150'),
('Amanda', 'Thompson', 'Psychology', 'Lecturer', 55000.00, 'a.thompson@university.edu', '2018-08-25', 'SS-320'),
('Kevin', 'White', 'Computer Science', 'Assistant Professor', 70000.00, 'k.white@university.edu', '2021-08-16', 'ENG-310'),
('Lisa', 'Hall', 'Mathematics', 'Associate Professor', 73000.00, 'l.hall@university.edu', '2014-01-12', 'SCI-205');

-- Populate Students (without specifying id - auto-generated)
INSERT INTO student (fname, lname, dept_name, major, tot_cred, email, enrollment_date, status) VALUES
('Alex', 'Johnson', 'Computer Science', 'Computer Science', 45, 'alex.johnson@student.edu', '2022-08-20', 'Active'),
('Emma', 'Williams', 'Computer Science', 'Software Engineering', 62, 'emma.williams@student.edu', '2021-08-15', 'Active'),
('Noah', 'Brown', 'Mathematics', 'Mathematics', 38, 'noah.brown@student.edu', '2023-01-10', 'Active'),
('Olivia', 'Davis', 'Physics', 'Physics', 55, 'olivia.davis@student.edu', '2021-08-20', 'Active'),
('Liam', 'Miller', 'English', 'English Literature', 72, 'liam.miller@student.edu', '2020-08-15', 'Active'),
('Sophia', 'Wilson', 'Business Administration', 'Business Administration', 48, 'sophia.wilson@student.edu', '2022-08-18', 'Active'),
('Mason', 'Moore', 'Biology', 'Biology', 41, 'mason.moore@student.edu', '2022-08-22', 'Active'),
('Isabella', 'Taylor', 'Psychology', 'Psychology', 67, 'isabella.taylor@student.edu', '2020-08-12', 'Active'),
('William', 'Anderson', 'Computer Science', 'Computer Science', 89, 'william.anderson@student.edu', '2019-08-15', 'Active'),
('Charlotte', 'Thomas', 'Mathematics', 'Applied Mathematics', 52, 'charlotte.thomas@student.edu', '2021-08-17', 'Active'),
('James', 'Jackson', 'Physics', 'Applied Physics', 76, 'james.jackson@student.edu', '2020-01-15', 'Active'),
('Amelia', 'White', 'English', 'Creative Writing', 34, 'amelia.white@student.edu', '2023-08-20', 'Active'),
('Benjamin', 'Harris', 'Business Administration', 'Finance', 58, 'benjamin.harris@student.edu', '2021-08-19', 'Active'),
('Mia', 'Martin', 'Biology', 'Pre-Med Biology', 43, 'mia.martin@student.edu', '2022-08-16', 'Active'),
('Lucas', 'Garcia', 'Psychology', 'Clinical Psychology', 81, 'lucas.garcia@student.edu', '2019-08-18', 'Active');

-- Populate Advisor relationships
INSERT INTO advisor (student_id, instructor_id, start_date) VALUES
(1, 1, '2022-08-20'),  -- Alex Johnson -> John Smith (CS)
(2, 2, '2021-08-15'),  -- Emma Williams -> Emily Davis (CS)
(3, 3, '2023-01-10'),  -- Noah Brown -> Michael Brown (Math)
(4, 4, '2021-08-20'),  -- Olivia Davis -> Sarah Wilson (Physics)
(5, 5, '2020-08-15'),  -- Liam Miller -> Robert Taylor (English)
(6, 6, '2022-08-18'),  -- Sophia Wilson -> Jessica Martinez (Business)
(7, 7, '2022-08-22'),  -- Mason Moore -> David Lee (Biology)
(8, 8, '2020-08-12'),  -- Isabella Taylor -> Amanda Thompson (Psychology)
(9, 1, '2019-08-15'),  -- William Anderson -> John Smith (CS)
(10, 10, '2021-08-17'), -- Charlotte Thomas -> Lisa Hall (Math)
(11, 4, '2020-01-15'), -- James Jackson -> Sarah Wilson (Physics)
(12, 5, '2023-08-20'), -- Amelia White -> Robert Taylor (English)
(13, 6, '2021-08-19'), -- Benjamin Harris -> Jessica Martinez (Business)
(14, 7, '2022-08-16'), -- Mia Martin -> David Lee (Biology)
(15, 8, '2019-08-18'); -- Lucas Garcia -> Amanda Thompson (Psychology)

-- Populate Courses
INSERT INTO course (course_id, title, credits, dept_name, description) VALUES
('CS101', 'Introduction to Programming', 3, 'Computer Science', 'Fundamentals of programming using Python'),
('CS102', 'Programming Fundamentals II', 3, 'Computer Science', 'Advanced programming concepts and algorithms'),
('CS201', 'Data Structures', 3, 'Computer Science', 'Implementation and analysis of fundamental data structures'),
('CS202', 'Advanced Data Structures', 3, 'Computer Science', 'Complex data structures and their applications'),
('CS301', 'Database Systems', 3, 'Computer Science', 'Design and implementation of database systems'),
('CS401', 'Software Engineering', 3, 'Computer Science', 'Principles and practices of large-scale software development'),
('CS501', 'Computer Networks', 3, 'Computer Science', 'Network protocols, architecture, and security'),
('MATH101', 'Calculus I', 4, 'Mathematics', 'Differential calculus and applications'),
('MATH102', 'Calculus with Applications', 4, 'Mathematics', 'Applied calculus for business and life sciences'), 
('MATH201', 'Calculus II', 4, 'Mathematics', 'Integral calculus and infinite series'),
('MATH301', 'Linear Algebra', 3, 'Mathematics', 'Vector spaces, matrices, and linear transformations'),
('MATH401', 'Differential Equations', 3, 'Mathematics', 'Ordinary and partial differential equations'),
('PHYS101', 'General Physics I', 4, 'Physics', 'Mechanics, waves, and thermodynamics'),
('PHYS201', 'General Physics II', 4, 'Physics', 'Electricity, magnetism, and optics'),
('PHYS301', 'Modern Physics', 3, 'Physics', 'Quantum mechanics and relativity'),
('ENG101', 'College Composition', 3, 'English', 'Academic writing and critical thinking'),
('ENG201', 'World Literature', 3, 'English', 'Survey of world literature from ancient to modern times'),
('ENG301', 'Advanced Writing', 3, 'English', 'Advanced composition and rhetoric'),
('BUS101', 'Introduction to Business', 3, 'Business Administration', 'Overview of business principles and practices'),
('BUS201', 'Accounting Principles', 3, 'Business Administration', 'Fundamentals of financial and managerial accounting'),
('BUS301', 'Marketing Management', 3, 'Business Administration', 'Marketing strategies and consumer behavior'),
('BIO101', 'General Biology', 4, 'Biology', 'Cell biology, genetics, and evolution'),
('BIO201', 'Organic Chemistry', 4, 'Biology', 'Structure and reactions of organic compounds'),
('BIO301', 'Molecular Biology', 3, 'Biology', 'Gene expression and protein synthesis'),
('PSY101', 'Introduction to Psychology', 3, 'Psychology', 'Overview of psychological principles and research methods'),
('PSY201', 'Research Methods', 3, 'Psychology', 'Statistical methods and experimental design in psychology'),
('PSY301', 'Cognitive Psychology', 3, 'Psychology', 'Mental processes including perception, memory, and learning');

-- Populate Prerequisites using the separate prereq table
INSERT INTO prereq (course_id, prereq_id) VALUES
-- Computer Science prerequisites
('CS201', 'CS101'),      -- Data Structures requires Intro Programming
('CS301', 'CS201'),      -- Database Systems requires Data Structures
('CS401', 'CS301'),      -- Software Engineering requires Database Systems
('CS501', 'CS201'),      -- Computer Networks requires Data Structures

-- Mathematics prerequisites
('MATH201', 'MATH101'),  -- Calculus II requires Calculus I
('MATH301', 'MATH201'),  -- Linear Algebra requires Calculus II
('MATH401', 'MATH201'),  -- Differential Equations requires Calculus II

-- Physics prerequisites
('PHYS201', 'PHYS101'),  -- General Physics II requires General Physics I
('PHYS201', 'MATH101'),  -- General Physics II requires Calculus I
('PHYS301', 'PHYS201'),  -- Modern Physics requires General Physics II
('PHYS301', 'MATH201'),  -- Modern Physics requires Calculus II

-- English prerequisites
('ENG201', 'ENG101'),    -- World Literature requires College Composition
('ENG301', 'ENG201'),    -- Advanced Writing requires World Literature

-- Business prerequisites
('BUS201', 'BUS101'),    -- Accounting requires Intro to Business
('BUS301', 'BUS201'),    -- Marketing requires Accounting

-- Biology prerequisites
('BIO201', 'BIO101'),    -- Organic Chemistry requires General Biology
('BIO301', 'BIO201'),    -- Molecular Biology requires Organic Chemistry

-- Psychology prerequisites
('PSY201', 'PSY101'),    -- Research Methods requires Intro Psychology
('PSY301', 'PSY201');    -- Cognitive Psychology requires Research Methods

-- Populate Sections for Fall 2024
INSERT INTO section (course_id, sec_id, semester, academic_year, time_slot, room, capacity, enrolled) VALUES
('CS101', '001', 'Fall', 2024, 'MWF 09:00-09:50', 'ENG-101', 30, 25),
('CS101', '002', 'Fall', 2024, 'TTh 14:00-15:15', 'ENG-102', 30, 28),
('CS201', '001', 'Fall', 2024, 'MWF 10:00-10:50', 'ENG-103', 25, 22),
('CS301', '001', 'Fall', 2024, 'TTh 10:00-11:15', 'ENG-104', 20, 18),
('CS401', '001', 'Fall', 2024, 'MWF 15:00-15:50', 'ENG-105', 15, 12),
('MATH101', '001', 'Fall', 2024, 'MWF 08:00-08:50', 'SCI-101', 35, 32),
('MATH101', '002', 'Fall', 2024, 'TTh 12:00-13:15', 'SCI-102', 35, 30),
('MATH201', '001', 'Fall', 2024, 'MWF 11:00-11:50', 'SCI-103', 30, 27),
('MATH301', '001', 'Fall', 2024, 'TTh 09:00-10:15', 'SCI-104', 25, 20),
('PHYS101', '001', 'Fall', 2024, 'TTh 08:00-09:15', 'PHY-101', 25, 23),
('PHYS201', '001', 'Fall', 2024, 'MWF 13:00-13:50', 'PHY-102', 20, 18),
('ENG101', '001', 'Fall', 2024, 'MWF 13:00-13:50', 'HUM-201', 25, 24),
('ENG201', '001', 'Fall', 2024, 'TTh 15:00-16:15', 'HUM-202', 20, 17),
('BUS101', '001', 'Fall', 2024, 'TTh 16:00-17:15', 'BUS-301', 40, 35),
('BUS201', '001', 'Fall', 2024, 'MWF 16:00-16:50', 'BUS-302', 30, 25),
('BIO101', '001', 'Fall', 2024, 'MWF 14:00-14:50', 'LS-101', 30, 28),
('BIO201', '001', 'Fall', 2024, 'TTh 13:00-14:15', 'LS-102', 25, 20),
('PSY101', '001', 'Fall', 2024, 'TTh 11:00-12:15', 'SS-201', 35, 31),
('PSY201', '001', 'Fall', 2024, 'MWF 12:00-12:50', 'SS-202', 25, 22);

-- Populate Spring 2025 sections (for demonstration)
INSERT INTO section (course_id, sec_id, semester, academic_year, time_slot, room, capacity, enrolled) VALUES
('CS102', '001', 'Spring', 2025, 'MWF 09:00-09:50', 'ENG-101', 30, 0),
('CS202', '001', 'Spring', 2025, 'TTh 14:00-15:15', 'ENG-102', 25, 0),
('MATH102', '001', 'Spring', 2025, 'MWF 10:00-10:50', 'SCI-101', 35, 0);

-- Populate Teaching assignments
INSERT INTO teaches (instructor_id, course_id, sec_id, semester, academic_year) VALUES
(1, 'CS101', '001', 'Fall', 2024),  -- John Smith teaches CS101-001
(2, 'CS101', '002', 'Fall', 2024),  -- Emily Davis teaches CS101-002
(1, 'CS201', '001', 'Fall', 2024),  -- John Smith teaches CS201-001
(2, 'CS301', '001', 'Fall', 2024),  -- Emily Davis teaches CS301-001
(9, 'CS401', '001', 'Fall', 2024),  -- Kevin White teaches CS401-001
(3, 'MATH101', '001', 'Fall', 2024), -- Michael Brown teaches MATH101-001
(10, 'MATH101', '002', 'Fall', 2024), -- Lisa Hall teaches MATH101-002
(3, 'MATH201', '001', 'Fall', 2024), -- Michael Brown teaches MATH201-001
(10, 'MATH301', '001', 'Fall', 2024), -- Lisa Hall teaches MATH301-001
(4, 'PHYS101', '001', 'Fall', 2024), -- Sarah Wilson teaches PHYS101-001
(4, 'PHYS201', '001', 'Fall', 2024), -- Sarah Wilson teaches PHYS201-001
(5, 'ENG101', '001', 'Fall', 2024),  -- Robert Taylor teaches ENG101-001
(5, 'ENG201', '001', 'Fall', 2024),  -- Robert Taylor teaches ENG201-001
(6, 'BUS101', '001', 'Fall', 2024),  -- Jessica Martinez teaches BUS101-001
(6, 'BUS201', '001', 'Fall', 2024),  -- Jessica Martinez teaches BUS201-001
(7, 'BIO101', '001', 'Fall', 2024),  -- David Lee teaches BIO101-001
(7, 'BIO201', '001', 'Fall', 2024),  -- David Lee teaches BIO201-001
(8, 'PSY101', '001', 'Fall', 2024),  -- Amanda Thompson teaches PSY101-001
(8, 'PSY201', '001', 'Fall', 2024);  -- Amanda Thompson teaches PSY201-001

-- Populate Student Enrollments (takes)
INSERT INTO takes (student_id, course_id, sec_id, semester, academic_year, cancelled, grade, enrollment_date) VALUES
-- Alex Johnson (student_id: 1) - CS major, freshman level
(1, 'CS101', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-20'),
(1, 'MATH101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-20'),
(1, 'ENG101', '001', 'Fall', 2024, FALSE, 'B', '2024-08-20'),

-- Emma Williams (student_id: 2) - CS major, intermediate level
(2, 'CS201', '001', 'Fall', 2024, FALSE, 'A', '2024-08-15'),
(2, 'MATH201', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-15'),
(2, 'PHYS101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-15'),

-- Noah Brown (student_id: 3) - Math major
(3, 'MATH101', '002', 'Fall', 2024, FALSE, 'A', '2024-01-10'),
(3, 'CS101', '002', 'Fall', 2024, FALSE, 'A-', '2024-01-10'),
(3, 'PHYS101', '001', 'Fall', 2024, FALSE, 'B+', '2024-01-10'),

-- Olivia Davis (student_id: 4) - Physics major
(4, 'PHYS201', '001', 'Fall', 2024, FALSE, 'A', '2024-08-20'),
(4, 'MATH201', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-20'),
(4, 'CS101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-20'),

-- Liam Miller (student_id: 5) - English major
(5, 'ENG201', '001', 'Fall', 2024, FALSE, 'A', '2024-08-15'),
(5, 'PSY101', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-15'),
(5, 'BUS101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-15'),

-- Sophia Wilson (student_id: 6) - Business major
(6, 'BUS201', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-18'),
(6, 'MATH101', '002', 'Fall', 2024, FALSE, 'B+', '2024-08-18'),
(6, 'ENG101', '001', 'Fall', 2024, FALSE, 'B', '2024-08-18'),

-- Mason Moore (student_id: 7) - Biology major
(7, 'BIO201', '001', 'Fall', 2024, FALSE, 'A', '2024-08-22'),
(7, 'MATH101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-22'),
(7, 'ENG101', '001', 'Fall', 2024, FALSE, 'B', '2024-08-22'),

-- Isabella Taylor (student_id: 8) - Psychology major
(8, 'PSY201', '001', 'Fall', 2024, FALSE, 'A', '2024-08-12'),
(8, 'MATH101', '002', 'Fall', 2024, FALSE, 'A-', '2024-08-12'),
(8, 'ENG101', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-12'),

-- William Anderson (student_id: 9) - Senior CS student
(9, 'CS401', '001', 'Fall', 2024, FALSE, 'A', '2024-08-15'),
(9, 'MATH301', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-15'),

-- Charlotte Thomas (student_id: 10) - Math major
(10, 'MATH301', '001', 'Fall', 2024, FALSE, 'A', '2024-08-17'),
(10, 'CS201', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-17'),

-- Add some cancelled enrollments and students taking prerequisites
(11, 'PHYS101', '001', 'Fall', 2024, TRUE, NULL, '2024-08-15'),  -- James Jackson cancelled
(12, 'ENG101', '001', 'Fall', 2024, FALSE, 'B-', '2024-08-20'), -- Amelia White completed
(13, 'BUS101', '001', 'Fall', 2024, FALSE, 'A-', '2024-08-19'), -- Benjamin Harris in intro course
(14, 'BIO101', '001', 'Fall', 2024, FALSE, 'B+', '2024-08-16'), -- Mia Martin taking prerequisite
(15, 'PSY101', '001', 'Fall', 2024, FALSE, 'A', '2024-08-18');  -- Lucas Garcia in intro course