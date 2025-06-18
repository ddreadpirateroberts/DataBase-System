import sqlite3
import os
import re
from typing import Any, Union, Optional, Dict, List, Tuple
from abc import ABC
from enum import Enum
from datetime import datetime


class Fetch(Enum): 
    ALL = "all"
    ONE = "one"

class InvalidEmail(Exception): ...

class UnsupportedDateFormat(Exception):
    def __init__(self, date: str):
        self.message = f"Date '{date}' is not in YYYY-MM-DD format or is invalid."
        super().__init__(self.message)

class IncorrectTimeslot(Exception): 
    def __init__(self, slot: str): 
        self.message = f"Timeslot {slot} is not of correct format. " \
                      "Example of an acceptable timeslot: TTh 14:00-15:15"
        super().__init__(self.message)
        
class IncorrectValue(Exception):
    def __init__(self, field: str, value: Any):
        self.message = f"The value '{value}' for field '{field}' is not valid."
        super().__init__(self.message)

class DataBaseError(Exception): 
    def __init__(self, error: str):
        super().__init__(error)

class RecordNotFound(Exception):
    def __init__(self, record_type: str, identifier: Any):
        self.message = f"{record_type} with identifier '{identifier}' not found."
        super().__init__(self.message)


class UniversityData(ABC):
    def __init__(self, db: str):
        self.db_path = os.path.join(os.path.dirname(__file__), db)
        exists = os.path.exists(self.db_path)
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON")      # By default, SQLite does not enforce foreign key constraints unless you explicitly turn them on.
        if not exists:
            self._read_ddl()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        self.conn.commit()
        self.conn.close()

    def _read_ddl(self):
        "loads the tables - ddl: data definition language"
        file_address = os.path.join(os.path.dirname(__file__), "ddl.sql")
        if not os.path.exists(file_address):
            raise FileNotFoundError("DDL file not found.")
        with open(file_address) as file:
            script = file.read()
            self.cursor.executescript(script)
        self.conn.commit()
        
    def _exec(self, query: str, params: Tuple = ()) -> bool: 
        """
        Execute a SQL query with parameters and commit the transaction.
        
        Args:
            query (str): SQL query string to execute
            params (tuple, optional): Query parameters for binding. Defaults to empty tuple.
        
        Returns:
            bool: True if query executed and committed successfully
            
        Raises:
            DataBaseError: If any SQLite error occurs during execution
        """
        if not isinstance(params, tuple): 
            params = (params,)
        try: 
            self.cursor.execute(query, params)
            self.conn.commit()
            if self.cursor.rowcount != -1: 
                print("Rows affected:", self.cursor.rowcount)
            return True
        except sqlite3.Error as e: 
            raise DataBaseError(e)
        
    def _select(self, query: str, params: Tuple = (), 
                fetch_type: Fetch = Fetch.ALL) -> Union[List[Tuple], Optional[Tuple]]:
        """Execute a SELECT query and return results"""
        if not isinstance(params, tuple): 
            params = (params,)
        try:
            self.cursor.execute(query, params)
            match fetch_type: 
                case Fetch.ALL: 
                    return self.cursor.fetchall()
                case Fetch.ONE: 
                    return self.cursor.fetchone()
                case _: 
                    raise ValueError(f"Invalid fetch_type: {fetch_type}")
        except sqlite3.Error as e:
            raise DataBaseError(e)
        
    def _check_query(self, table: str, column: str, value: Any) -> bool:
        """
        Check if a record exists in the specified table.
        
        Args:
            table (str): Name of the database table to query
            field (str): Column name to check against  
            value: Value to search for in the specified field
            
        Returns:
            bool: True if at least one matching record exists, False otherwise
        """
        check_query = f"""SELECT COUNT(*) FROM {table} WHERE {column} = ?"""
        exists = self._select(check_query, value, Fetch.ONE)[0] != 0
        return exists

    # ---------------- validation methods -----------------
    def _validate_email(self, email: str):
        if not re.match(r"[^@]+@[^@]+\.[^@]+$", email):
            raise InvalidEmail()
    
    def _validate_semester(self, sem: str):
        if sem not in ['Fall', 'Winter', 'Spring', 'Summer']:
            raise IncorrectValue("semester", sem)

    def _validate_salary(self, amount: Union[float, str]):
        try:
            amount = float(amount)
            if amount < 0:
                raise IncorrectValue("salary", amount)
        except ValueError:
            raise IncorrectValue("salary", amount)
        
    def _validate_date(self, date: str):
        pattern = r"^[\d]{4}-[\d]{2}-[\d]{2}$"
        if re.match(pattern, date):
            _, month, day = map(int, date.split('-'))
            has_days = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
                        7:31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
            if month in has_days and 0 < day <= has_days[month]:
                return 
        raise UnsupportedDateFormat(date)
          
    def _validate_status(self, status: str):
        if status not in ['Active', 'Inactive', 'Graduated', 'Suspended']:
            raise IncorrectValue("status", status)
    
    def _validate_grade(self, grade: str):
        valid_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'F']
        if grade not in valid_grades:
            raise IncorrectValue("grade", grade)
    
    def _validate_rank(self, rank: str): 
        valid_ranks = ['Assistant Professor', 'Associate Professor', 'Professor', 'Lecturer', 'Adjunct']
        if rank not in valid_ranks: 
            raise IncorrectValue("academic rank", rank)
    
    def _validate_credit(self, cred: int): 
        if isinstance(cred, int): 
            if 0 < cred < 5: 
                return 
            raise IncorrectValue("credit", cred)
        raise ValueError("credits should be an integer")
    
    def _validate_academic_year(self, year: int): 
        if isinstance(year, int): 
            if 1701 < year < 2100: 
                return
            raise IncorrectValue("academic_year", year)
        raise ValueError("academic_year should be an integer")
    
    def _validate_timeslot(self, slot: str):
        day_pattern = r"([MTWFS]|Th|Su|TTh|MWF|MW|TR|WF)"
        hhmm_pattern = r"([01]?[0-9]|2[0-3]):[0-5][0-9]"
        pattern = rf'^{day_pattern}\s{hhmm_pattern}-{hhmm_pattern}$'
        if not re.match(pattern, slot): 
            raise IncorrectTimeslot(slot)
        
    
class AdminQueryHandler(UniversityData):
    def __init__(self, db):
        super().__init__(db)

    # ---------------- department management -------------------
    def create_dept(self, dept_name: str, phone: str, budget: float,
                    building: str, dean_name: str) -> bool:
        """Create a new department"""
        query = "INSERT INTO department VALUES(?, ?, ?, ?, ?)"
        return self._exec(query, (dept_name, phone, budget, building, dean_name))
    
    def update_dept(self, dept_name: str, **updates) -> bool:
        """
        Update department information
        
        Args:
            dept_name (str): Name of the department to update
            **updates: Keyword arguments for fields to update (e.g., building='Main', budget=50000)
        
        Returns:
            bool: True if department was updated successfully, False if not found
            
        Raises:
            RecordNotFound: If department not found
            DataBaseError: If database error occurs
            ValueError: If no updates provided or invalid field names
        """
        dept_exists = self._check_query(table="department", column="dept_name", value=dept_name)
        if not dept_exists: 
            raise RecordNotFound("Department", dept_name)
        
        if not updates:
            raise ValueError("No updates provided")
        
        valid = {"phone", "budget", "building", "dean_name"}
        
        invalid = set(updates.keys()) - valid
        if invalid:
            raise ValueError(f"Invalid field names: {invalid}")
        
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        query = f"UPDATE department SET {set_clause} WHERE dept_name = ?"
        params = tuple(updates.values()) + (dept_name,)
        
        return self._exec(query, params)
    
    def delete_dept(self, dept_name: str) -> bool: 
        """Delete department (check RESTRICT constraint)"""
        exists = self._check_query(table="department", column="dept_name", value=dept_name)
        if not exists: 
            raise RecordNotFound("Department", dept_name)
        query = "DELETE FROM department WHERE dept_name = ?"
        return self._exec(query, dept_name)
    
    def get_dept_info(self, dept_name: str) -> Optional[Tuple]:
        """Get department information"""
        query = "SELECT * FROM department WHERE dept_name = ?"
        return self._select(query, dept_name, Fetch.ONE)
    
    def get_all_depts(self) -> List[tuple]:
        """Get all departments"""
        query = "SELECT * FROM department"
        return self._select(query) 
    
    # ---------------- student management ---------------------
    def create_student(self, fname: str, lname: str, dept_name: str, email: str,
                       *, tot_cred: int = 0, major: str = None,
                       enrollment_date: str = None) -> int:
        """
        Create a new student record.

        Parameters:
            fname (str): First name of the student.
            lname (str): Last name of the student.
            dept_name (str): Department name the student belongs to.
            email (str): Student's email address.
            tot_cred (int, optional): Total credits earned. Defaults to 0.
            major (str, optional): Major subject.
            enrollment_date (str, optional): Date of enrollment (e.g., '2025-09-01').

        Returns:
            int: ID of the newly created student.
        """        
        self._validate_email(email)
        if enrollment_date: 
            self._validate_date(enrollment_date)

        dept_exists = self._check_query(table="department", column="dept_name", value=dept_name)
        if not dept_exists:
            raise RecordNotFound("Department", dept_name)

        columns = ["fname", "lname", "dept_name", "email", "tot_cred", "major"]
        values = [fname, lname, dept_name, email, tot_cred, major]
        
        if enrollment_date:
            columns.append("enrollment_date")
            values.append(enrollment_date)
       
        qmarks =  ["?"] * len(values)
        query = f"INSERT INTO student ({', '.join(columns)}) VALUES ({', '.join(qmarks)})"
        
        self._exec(query, tuple(values))
        return self.cursor.lastrowid    
    
    def update_student(self, student_id: int, **updates) -> bool:
        """Update student information -- student_id is unchangeable"""
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists: 
            raise RecordNotFound("Student", student_id)
        
        if "status" in updates.keys(): 
            self._validate_status(updates["status"])
        if "email" in updates.keys(): 
            self._validate_email(updates["email"])
        if "enrollment_date" in updates.keys(): 
            self._validate_date(updates["enrollment_date"])
        
        valid = {
            "fname", "lname", "dept_name", 
            "major", "tot_cred", "email", 
            "enrollment_date", "status"
        }
        
        invalid = set(updates.keys()) - valid 
        if invalid: 
            raise ValueError(f"invalid field arg: {invalid}")
        
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()]) 
        query = f"UPDATE student SET {set_clause} WHERE id = ?"
        params = tuple(updates.values()) + (student_id,)
        
        return self._exec(query, params)
    
    def delete_student(self, student_id: int) -> bool:
        """Delete student"""
        exists = self._check_query(table="student", column="id", value=student_id)
        if not exists: 
            raise RecordNotFound("Student", student_id)   
        query = "DELETE FROM student WHERE id = ?"
        return self._exec(query, student_id)
            
    def get_student_info(self, student_id: int) -> Optional[Tuple]:
        """Get student information"""
        query = "SELECT * FROM student WHERE id = ?"
        return self._select(query, student_id, Fetch.ONE)
 
    def get_all_students(self, dept_name: Optional[str] = None) -> List[Tuple]:
        """Get all students, optionally filtered by department"""
        if dept_name: 
            query = "SELECT * FROM student WHERE dept_name = ?"
            result = self._select(query, dept_name)
        else: 
            result = self._select("SELECT * FROM student")
            
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]
    
    def search_students(self, **criteria) -> List[Tuple]:
        """Search students by various criteria (name, email, major, etc.)"""
        
        valid = {
            "id", "fname", "lname", 
            "dept_name", "major", "tot_cred", 
            "email", "enrollment_date", "status"
        }
        
        invalid = set(criteria.keys()) - valid
        if invalid: 
            raise ValueError(f"invalid field arg: {invalid}")
        
        where_clause = " and ".join([f"{field} = ?" for field in criteria.keys()])
        query = f"SELECT * FROM student WHERE {where_clause}"
        params = tuple(criteria.values())
        
        return self._select(query, params)
                
    def get_student_transcript(self, student_id: int) -> List[Dict]:
        query = """
            SELECT t.course_id, c.title, c.credits, t.semester, t.academic_year, 
                t.grade, t.enrollment_date
            FROM takes t
            JOIN course c ON t.course_id = c.course_id
            WHERE t.student_id = ? AND t.cancelled = FALSE AND t.grade IS NOT NULL
            ORDER BY t.academic_year, t.semester, t.course_id
        """
        result = self._select(query, student_id)
        
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]

        
    def calculate_gpa(self, student_id: int) -> float: 
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        
        query = """
            SELECT c.credits, t.grade
            FROM takes t
            JOIN course c ON t.course_id = c.course_id
            WHERE t.student_id = ? AND t.grade IS NOT NULL
        """
        info = self._select(query, student_id)
        
        total_points = 0
        total_credits = 0
        
        for credits, grade in info:
            total_points += credits * grade_points[grade]
            total_credits += credits
        
        return total_points / total_credits if total_credits > 0 else 0
    
    # ---------------- Instructor Management --------------------
    def create_instructor(self, fname: str, lname: str, dept_name: str, email: str,
                         academic_rank: str, salary: float, hire_date: Optional[str] = None,
                         office_number: Optional[str] = None) -> int:
        """Create a new instructor record"""
        
        self._validate_email(email)
        self._validate_rank(academic_rank)
        self._validate_salary(salary)
        if hire_date: 
            self._validate_date(hire_date)
            
        dept_exists = self._check_query(table="department", column="dept_name", value=dept_name)
        if not dept_exists:
            raise RecordNotFound("Department", dept_name)

        columns = ["fname", "lname", "dept_name", "email", "academic_rank", "salary", "office_number"]
        values = [fname, lname, dept_name, email, academic_rank, salary, office_number]
        
        if hire_date:
            columns.append("hire_date")
            values.append(hire_date)
        
        qmarks = ["?"] * len(values)
        query = f"INSERT INTO instructor ({', '.join(columns)}) VALUES ({', '.join(qmarks)})"
        
        self._exec(query, tuple(values))
        return self.cursor.lastrowid    

    def update_instructor(self, instructor_id: int, **updates) -> bool:
        """Update instructor information"""
        
        instructor_exists = self._check_query(table="instructor", column="id", value=instructor_id)
        if not instructor_exists: 
            raise RecordNotFound("Instructor", instructor_id)
        
        if "academic_rank" in updates.keys(): 
            self._validate_rank(updates["academic_rank"])
        if "email" in updates.keys(): 
            self._validate_email(updates["email"])
        if "hire_date" in updates.keys(): 
            self._validate_date(updates["hire_date"])
        if "salary" in updates.keys(): 
            self._validate_salary(updates["salary"])
        
        valid = {
            "fname", "lname", "dept_name", 
            "academic_rank", "salary", "email", 
            "hire_date", "office_number"
        }
        
        invalid = set(updates.keys()) - valid 
        if invalid: 
            raise ValueError(f"invalid field arg: {invalid}")
        
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])    
        query = f"UPDATE instructor SET {set_clause} WHERE id = ?"
        params = tuple(updates.values()) + (instructor_id,)
        
        return self._exec(query, params)
    
    def delete_instructor(self, instructor_id: int) -> bool:
        """Delete instructor record"""
        exists = self._check_query(table="instructor", column="id", value=instructor_id)
        if not exists: 
            raise RecordNotFound("Instructor", instructor_id)
        query = "DELETE FROM instructor WHERE id = ?"
        return self._exec(query, instructor_id)
        
    def get_instructor_info(self, instructor_id: int) -> Optional[Tuple]:
        """Get instructor information"""
        query = "SELECT * FROM instructor WHERE id = ?"
        return self._select(query, instructor_id, Fetch.ONE)
     
    def get_all_instructors(self, dept_name: Optional[str] = None) -> List[Tuple]:
        """Get all instructors, optionally filtered by department"""
        if dept_name: 
            query = "SELECT * FROM instructor WHERE dept_name = ?"
            result = self._select(query, dept_name)
        else: 
            result = self._select("SELECT * FROM instructor")
            
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]
    
    def get_instructor_workload(self, instructor_id: int, semester: str, year: int) -> List[Dict]:
        """Get instructor's teaching workload for a semester"""
        query = """
            SELECT t.course_id, t.sec_id, s.time_slot, s.room
            FROM teaches t
            JOIN section s ON t.course_id = s.course_id 
                           AND t.sec_id = s.sec_id 
                           AND t.semester = s.semester 
                           AND t.academic_year = s.academic_year
            WHERE t.instructor_id = ? AND t.semester = ? AND t.academic_year = ?
        """
        params = (instructor_id, semester, year)
        result = self._select(query, params)
        
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]
        
    # ---------------- Course Management --------------------
    def create_course(self, course_id: str, title: str, credits: int,
                     dept_name: str, description: Optional[str] = None) -> bool:
        """Create a new course"""
        self._validate_credit(credits)
        query = f"""INSERT INTO course VALUES (?, ?, ?, ?, ?)"""
        params = (course_id, title, credits, dept_name, description)
        return self._exec(query, params)
    
    def update_course(self, course_id: str, **updates) -> bool:
        """Update course information"""
        
        if "credits" in updates.keys(): 
            self._validate_credit(updates["credits"]) 
            
        valid = {"title", "credits", "dept_name", "description"}   
        
        invalid = set(updates.keys()) - valid 
        if invalid: 
            raise ValueError(f"invalid field arg: {invalid}")

        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        query = f"UPDATE course SET {set_clause} WHERE course_id = ?"
        params = tuple(updates.values()) + (course_id, )
        
        return self._exec(query, params)
                    
    def delete_course(self, course_id: str) -> bool:
        """Delete course"""
        exists = self._check_query(table="course", column="course_id", value=course_id)
        if not exists: 
            raise RecordNotFound("Course", course_id)
        query = "DELETE FROM course WHERE course_id = ?"
        return self._exec(query, course_id)
    
    def get_course_info(self, course_id: str) -> Optional[Tuple]:
        """Get course information with prerequisites"""
        query = "SELECT * FROM course WHERE course_id = ?"
        return self._select(query, course_id, Fetch.ONE)
    
    def get_all_courses(self, dept_name: Optional[str] = None) -> List[Dict]:
        """Get all courses, optionally filtered by department"""
        if dept_name: 
            query = 'SELECT * FROM course WHERE dept_name = ?'
            result = self._select(query, dept_name, Fetch.ALL)
        else: 
            result = self._select('SELECT * FROM course')
        
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]
    
    def add_prerequisite(self, course_id: str, prereq_id: str) -> bool:
        """Add a prerequisite to a course"""
        src_exists = self._check_query(table="course", column="course_id", value=course_id)
        if not src_exists:  
            raise RecordNotFound("Course", course_id)
        prq_exists = self._check_query(table="course", column="course_id", value=prereq_id)
        if not prq_exists: 
            raise RecordNotFound("Course", prereq_id) 
        query = "INSERT INTO prereq VALUES (?, ?)"
        return self._exec(query, (course_id, prereq_id))
    
    def remove_prerequisite(self, course_id: str, prereq_id: str) -> bool:
        """Remove a prerequisite from a course"""
        src_exists = self._check_query(table="course", column="course_id", value=course_id)
        if not src_exists:  
            raise RecordNotFound("Course", course_id)
        prq_exists = self._check_query(table="course", column="course_id", value=prereq_id)
        if not prq_exists: 
            raise RecordNotFound("Course", prereq_id) 
        query = "DELETE FROM prereq WHERE course_id = ? AND prereq_id = ?"
        return self._exec(query, (course_id, prereq_id))

    def get_prerequisite(self, course_id: str) -> List: 
        """Get all prerequisites for a course"""
        query = "SELECT * FROM prereq WHERE course_id = ?"
        return self._select(query, course_id)
    
    # ---------------- Section Management --------------------
    def create_section(self, course_id: str, sec_id: str, sem: str, 
                       year: int, time_slot: str, room: str, capacity: int) -> bool:
        """Create a new course section"""
        
        course_exists = self._check_query(table="course", column="course_id", value=course_id)
        if not course_exists: 
            raise RecordNotFound("Course", course_id)    # if not handled, rasies a foreign key error 
        
        self._validate_semester(sem)
        self._validate_academic_year(year)
        self._validate_timeslot(time_slot)
        if capacity <= 0: 
            raise IncorrectValue("capacity", capacity)
        
        qmarks = ", ".join(["?"]*8)
        query = "INSERT INTO section VALUES ({content})".format(content=qmarks)
        params = (course_id, sec_id, sem, year, time_slot, room, capacity, 0)
        return self._exec(query, params)
    
    def update_section(self, course_id: str, sec_id: str, sem: str, 
                       year: int, **updates) -> bool:
        """Update section information"""
        
        params = (course_id, sec_id, sem, year)

        check_query = """
            SELECT COUNT(*) 
            FROM section 
            WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
        """
        
        self.cursor.execute(check_query, params)
        section_exists = self.cursor.fetchone()[0]
        
        if not section_exists: 
            raise RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}")
        
        valid = {"time_slot", "room", "capacity", "enrolled"}
        
        invalid = set(updates.keys()) - valid 
        if invalid: 
            raise ValueError(f"invalid field arg: {invalid}")
        
        set_clause = ", ".join([f"{field} = ?" for field in updates.keys()])
        
        query = f"""
            UPDATE section 
            SET {set_clause}
            WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
        """

        params = tuple(updates.values()) + (course_id, sec_id, sem, year)

        return self._exec(query, params)
    
    def delete_section(self, course_id: str, sec_id: str, sem: str, year: int) -> bool:
        """Delete section"""
        
        params = (course_id, sec_id, sem, year)

        check_query = """
            SELECT COUNT(*) 
            FROM section 
            WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
        """
        
        self.cursor.execute(check_query, params)
        section_exists = self.cursor.fetchone()[0]
        
        if not section_exists: 
            return RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}") 
        
        delete_query = """
            DELETE FROM section 
            WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
        """
        
        return self._exec(delete_query, params)
    
    def assign_instructor(self, instructor_id: int, course_id: str, sec_id: str, 
                          sem: str, year: int) -> bool:
        """Assign instructor to a section"""
        
        self._validate_semester(sem)
        self._validate_academic_year(year)
        
        check_query = """
            SELECT COUNT(*)
            FROM section
            WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
        """
        self.cursor.execute(check_query, (course_id, sec_id, sem, year))
        sec_exists = self.cursor.fetchone()[0]
        if not sec_exists: 
            raise RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}")
        
        instructor_exists = self._check_query(table="instructor", column="id", value=instructor_id)
        if not instructor_exists:
            raise RecordNotFound("Instructor", instructor_id)
        
        params = (instructor_id, course_id, sec_id, sem, year)
        query = "INSERT INTO teaches VALUES (?, ?, ?, ?, ?)"
        
        return self._exec(query, params)
    
    def unassign_instructor(self, instructor_id: int, course_id: str, sec_id: str,
                            sem: str, year: int) -> bool:
        """Remove instructor from a section"""
        
        check_query = """
            SELECT COUNT(*)
            FROM teaches 
            WHERE instructor_id = ? AND course_id = ? AND sec_id = ? 
                AND semester = ? AND academic_year = ? 
         """
         
        self.cursor.execute(check_query, (instructor_id, course_id, sec_id, sem, year))
        exists = self.cursor.fetchone()[0]
        if not exists:
            raise RecordNotFound(
                "Teaches", 
                f"{instructor_id}-{course_id}-{sec_id}-{sem}-{year}"
            )
        
        params = (instructor_id, course_id, sec_id, sem, year)
        delete_query = """
            DELETE FROM teaches
            WHERE instructor_id = ? AND course_id = ? AND sec_id = ?
                AND semester = ? AND academic_year = ?
        """
        
        return self._exec(delete_query, params)

    def get_section_info(self, course_id: str, sec_id: str, sem: str, year: int) -> Optional[Dict]:
        """Get section information with enrollment details"""
        
        query = """
            SELECT s.course_id, s.sec_id, s.semester, s.academic_year, 
                   s.time_slot, s.room, s.capacity, s.enrolled,
                   i.fname || ' ' || i.lname AS instructor_name
            FROM section s
            LEFT JOIN teaches t ON s.course_id = t.course_id 
                                AND s.sec_id = t.sec_id 
                                AND s.semester = t.semester 
                                AND s.academic_year = t.academic_year
            LEFT JOIN instructor i ON t.instructor_id = i.id
            WHERE s.course_id = ? AND s.sec_id = ? AND s.semester = ? AND s.academic_year = ?
            ORDER BY s.academic_year, s.semester, s.course_id, s.sec_id
        """
        params = (course_id, sec_id, sem, year)
        result = self._select(query, params, Fetch.ONE)
        
        if result:
            column_names = [col[0] for col in self.cursor.description]
            return dict(zip(column_names, result))
        return None
    
    def get_all_sections(self, sem: str = None, year: int = None) -> List[Dict]:
        """Get all sections with course and instructor details optionally filtered by semester and/or year"""
        
        query = """
            SELECT s.course_id, s.sec_id, s.semester, s.academic_year,
                s.time_slot, s.room, s.capacity, s.enrolled,
                c.title, c.credits, c.dept_name,
                i.fname || ' ' || i.lname AS instructor_name,
                i.id AS instructor_id
            FROM section s
            JOIN course c ON s.course_id = c.course_id
            LEFT JOIN teaches t ON s.course_id = t.course_id 
                                AND s.sec_id = t.sec_id 
                                AND s.semester = t.semester 
                                AND s.academic_year = t.academic_year
            LEFT JOIN instructor i ON t.instructor_id = i.id
        """
        
        params = []
        conditions = []
        
        if sem is not None:
            self._validate_semester(sem)
            conditions.append("s.semester = ?")
            params.append(sem)
        
        if year is not None:
            self._validate_academic_year(year)
            conditions.append("s.academic_year = ?")
            params.append(year)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY s.academic_year, s.semester, s.course_id, s.sec_id"
        
        result = self._select(query, tuple(params))
        
        column_names = [col[0] for col in self.cursor.description]
        return [dict(zip(column_names, row)) for row in result]
    
    # ---------------- Enrollment Management --------------------
    def enroll_student(self, student_id: int, course_id: str, sec_id: str,
                       sem: str, year: int) -> bool:
        """Enroll student in a section"""
        
        def section_is_active(sec: Dict) -> bool:
            now = datetime.now()
            month = now.month
            if month in [1, 2]:
                current_month = "Winter"
            elif month in [3, 4, 5]:
                current_month = "Spring"  
            elif month in [6, 7, 8]:
                current_month = "Summer"
            else:  
                current_month = "Fall"
            return sec["semester"] == current_month and sec["academic_year"] == now.year

        section = self.get_section_info(course_id, sec_id, sem, year)
        if not section:
            raise RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}")
        if section["enrolled"] >= section["capacity"]:
            raise ValueError("Section is full")
        
        if not section_is_active(section):
            raise ValueError("Section is not active")
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists:
            raise RecordNotFound("Student", student_id)
        
        self._validate_semester(sem)
        self._validate_academic_year(year)

        params = (student_id, course_id, sec_id, sem, year)
        query = """
            INSERT INTO takes (student_id, course_id, sec_id, semester, academic_year, cancelled)
            VALUES (?, ?, ?, ?, ?, FALSE)
        """

        if self._exec(query, params):
            update_query = """
                UPDATE section 
                SET enrolled = enrolled + 1 
                WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
            """
            return self._exec(update_query, (course_id, sec_id, sem, year))
        
        return False
    
    def get_enrollment_info(self, student_id: int, course_id: str, 
                            sec_id: str, sem: str, year: int) -> Optional[Dict]:
        """Get enrollment information for a student in a section"""
        
        query = """
            SELECT st.fname || ' ' || st.lname AS student_name,
                   t.student_id, t.course_id, t.sec_id, t.semester, t.academic_year,
                   t.cancelled, t.enrollment_date, t.grade,
                   s.time_slot, s.room
            FROM takes t
            LEFT JOIN section s ON t.course_id = s.course_id 
                                AND t.sec_id = s.sec_id 
                                AND t.semester = s.semester 
                                AND t.academic_year = s.academic_year
            LEFT JOIN student st ON t.student_id = st.id
            WHERE t.student_id = ? AND t.course_id = ? AND t.sec_id = ? 
                  AND t.semester = ? AND t.academic_year = ?
        """
        params = (student_id, course_id, sec_id, sem, year)
        result = self._select(query, params, Fetch.ONE)
        if result:
            column_names = [col[0] for col in self.cursor.description]
            return dict(zip(column_names, result))
    
    def drop_student(self, student_id: int, course_id: str, sec_id: str,
                     sem: str, year: int) -> bool:
        """Drop student from a section"""
        
        section = self.get_section_info(course_id, sec_id, sem, year)
        if not section:
            raise RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}")
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists:
            raise RecordNotFound("Student", student_id)
        
        check_query = """
            SELECT COUNT(*)
            FROM takes
            WHERE student_id = ? AND course_id = ? AND sec_id = ? 
                  AND semester = ? AND academic_year = ?
        """
        self.cursor.execute(check_query, (student_id, course_id, sec_id, sem, year))
        is_enrolled = self.cursor.fetchone()[0]
        if not is_enrolled:
            return False

        params = (student_id, course_id, sec_id, sem, year) 
        query = """
            DELETE FROM takes
            WHERE student_id = ? AND course_id = ? AND sec_id = ? 
                  AND semester = ? AND academic_year = ?
        """
        
        if self._exec(query, params):
            update_query = """
                UPDATE section 
                SET enrolled = enrolled - 1 
                WHERE course_id = ? AND sec_id = ? AND semester = ? AND academic_year = ?
            """
            return self._exec(update_query, (course_id, sec_id, sem, year))
            
    def assign_grade(self, student_id: int, course_id: str, sec_id: str,
                     sem: str, year: int, grade: str) -> bool:
        """Assign grade to student for a course"""
    
        section = self.get_section_info(course_id, sec_id, sem, year)
        if not section:
            raise RecordNotFound("Section", f"{course_id}-{sec_id}-{sem}-{year}")
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists:
            raise RecordNotFound("Student", student_id)
        
        params = (student_id, course_id, sec_id, sem, year)
        check_query = """
            SELECT COUNT(*)
            FROM takes
            WHERE student_id = ? AND course_id = ? AND sec_id = ?
                  AND semester = ? AND academic_year = ?
        """
        take_record_exists = self.cursor.execute(check_query, params).fetchone()[0]
        if not take_record_exists:
            raise RecordNotFound("Takes", f"{student_id}-{course_id}-{sec_id}-{sem}-{year}")
        
        self._validate_grade(grade)
        self._validate_semester(sem)
        self._validate_academic_year(year)

        query = """
            UPDATE takes
            SET grade = ?
            WHERE student_id = ? AND course_id = ? AND sec_id = ?
                  AND semester = ? AND academic_year = ?
        """
        params = (grade, student_id, course_id, sec_id, sem, year)
        return self._exec(query, params)
    
    # ---------------- Advisor Management --------------------
    def assign_advisor(self, student_id: int, instructor_id: int,
                       start_date: Optional[str] = None) -> bool:
        """Assign advisor to student"""
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists: 
            raise RecordNotFound("Student", student_id)
        
        instructor_exists = self._check_query(table="instructor", column="id", value=instructor_id)
        if not instructor_exists: 
            raise RecordNotFound("Instructor", instructor_id)
        
        params = (student_id, instructor_id)
        columns = ["student_id", "instructor_id"]
        
        if start_date: 
            params += (start_date,)
            columns.append("start_date")
            
        column_clause = ", ".join(columns)
        qmarks = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO advisor({column_clause}) VALUES ({qmarks})"  
         
        return self._exec(query, params)
        
    def update_advisor(self, student_id: int, new_instructor_id: int,
                    end_date: Optional[str] = None) -> bool:
        """Change student's advisor or unassign current advisor"""
        
        student_exists = self._check_query(table="student", column="id", value=student_id)
        if not student_exists:
            raise RecordNotFound("Student", student_id)
        
        instructor_exists = self._check_query(table="instructor", column="id", value=new_instructor_id)
        if not instructor_exists:
            raise RecordNotFound("Instructor", new_instructor_id)
        
        if end_date:
            self._validate_date(end_date)
                
        update_query = """
            UPDATE advisor SET instructor_id = ?, end_date = ? 
            WHERE student_id = ?
        """
        
        return self._exec(update_query, (new_instructor_id, end_date, student_id))
         
    def get_advisor_info(self, student_id: int) -> Optional[Dict]:
        """Get current advisor information for a student"""
        
        query = """
            SELECT  s.fname || " " || s.lname AS student_name, 
                    a.student_id, 
                    i.fname || " " || i.lname AS advisor_name, 
                    i.email AS advisor_email, i.office_number AS advisor_office_number, 
                    a.start_date, a.end_date
            FROM advisor a 
            LEFT JOIN student s ON s.id = a.student_id
            LEFT JOIN instructor i ON i.id = a.instructor_id
            WHERE a.student_id = ?
        """
        result = self._select(query, student_id, Fetch.ONE)
        
        if result:
            column_names = [col[0] for col in self.cursor.description]
            return dict(zip(column_names, result))


def populate(db: UniversityData, script_file: str):
    script_file = os.path.join(os.path.dirname(__file__), script_file)
    with open(script_file) as file:
        script = file.read()
        db.cursor.executescript(script)
    db.conn.commit()


if __name__ == "__main__":
    with AdminQueryHandler("university.db") as db:
        # populate(db, 'populate.sql')
        # db.cursor.execute('drop table department')
        pass
