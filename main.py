#discription: This is the main file of the program. It is responsible for the initialization of the database and the start of the program.
from db_conn import DB_CONN
from menu import Menu


TEACHER_STATMENT = """
CREATE TABLE IF NOT EXISTS teachers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);"""

STUDENT_STATMENT = """ CREATE TABLE IF NOT EXISTS students (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  email TEXT NOT NULL
);"""

COURSE_STATMENT = """ CREATE TABLE IF NOT EXISTS courses (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  teacher_id INTEGER NOT NULL,
  FOREIGN KEY (teacher_id) REFERENCES teachers(id)
);"""

ENROLLMENT_STATMENT = """ CREATE TABLE IF NOT EXISTS enrollments (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  grade INTEGER,
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (course_id) REFERENCES courses(id)
);"""

TEACHER_STATMENT = """
INSERT INTO teachers(name, email) 
VALUES ("Mark", "mark@gmail.com"), 
       ("Anthony", "anthony@gmail.com"), 
       ("Peter", "peter@gmail.com"), 
       ("Thomas", "thomas@gmail.com");"""



class Main:
    def __init__(self) -> None:
        print("Program starts.")
        self.initDatabase()
        menu = Menu()
        menu.start()
        DB_CONN.close()
        print("Program ends.")
        return None
    
    def initDatabase(self) -> None:
        cursor = DB_CONN.cursor()
        
        cursor.execute(TEACHER_STATMENT)
        cursor.execute(STUDENT_STATMENT)
        cursor.execute(COURSE_STATMENT)
        cursor.execute(ENROLLMENT_STATMENT)
        cursor.execute(TEACHER_STATMENT)
        
        DB_CONN.commit()
        cursor.close()
        return None
    
if __name__ == "__main__":
    app = Main()