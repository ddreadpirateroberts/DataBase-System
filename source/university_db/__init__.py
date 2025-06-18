"""
University Database Management System

A comprehensive database handler for managing university data including students,
instructors, courses, sections, enrollments, and academic records.

Example usage:
    from university_db import AdminQueryHandler
    
    with AdminQueryHandler("university.db") as db:
        # Create a department
        db.create_dept("Computer Science", "555-0123", 100000.0, "Tech Building", "Dr. Smith")
        
        # Create a student
        student_id = db.create_student("John", "Doe", "Computer Science", "john.doe@university.edu")
        
        # Get student info
        student = db.get_student_info(student_id)
        print(f"Student: {student}")
"""

from .db_handler import (
    AdminQueryHandler,
    UniversityData,
    Fetch,
    InvalidEmail,
    UnsupportedDateFormat,
    IncorrectTimeslot,
    IncorrectValue,
    DataBaseError,
    RecordNotFound,
    populate
)

__version__ = "1.0.0"

# Package metadata
__all__ = [
    # Main classes
    "AdminQueryHandler",
    "UniversityData",
    
    # Enums
    "Fetch",
    
    # Exceptions
    "InvalidEmail",
    "UnsupportedDateFormat", 
    "IncorrectTimeslot",
    "IncorrectValue",
    "DataBaseError",
    "RecordNotFound",
    
    # Utilities
    "populate"
]

# Package level constants
DEFAULT_DB_NAME = "university.db"
SUPPORTED_SEMESTERS = ["Fall", "Winter", "Spring", "Summer"]
VALID_GRADES = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D+", "D", "F"]
VALID_RANKS = ["Assistant Professor", "Associate Professor", "Professor", "Lecturer", "Adjunct"]
VALID_STATUSES = ["Active", "Inactive", "Graduated", "Suspended"]

def get_version():
    """Return the current version of the university database package."""
    return __version__

def create_database(db_path: str = None):
    """
    Convenience function to create a new university database.
    
    Args:
        db_path (str, optional): Path to database file. Defaults to 'university.db'
        
    Returns:
        AdminQueryHandler: Database handler instance
        
    Example:
        db = create_database("my_university.db")
        with db:
            # Use database operations
            pass
    """
    if db_path is None:
        db_path = DEFAULT_DB_NAME
    return AdminQueryHandler(db_path)
