# Description: Menu class for the student management system
#This class is responsible for displaying the menu and handling user input. and it is also responsible for calling the appropriate methods in the Student class to perform the required actions.


from db_conn import DB_CONN


class Menu:
    def __init__(self) -> None:
        return None
    
    def askChoice(self) -> str:
        print("1. Add new student")
        print("2. View student records")
        print("3. Update student records")
        print("4. Add new course")
        print("5. View course list")
        print("6. Enroll student in a course")
        print("7. View student's enrolled courses")
        print("0. Exit")
        
        choice = input("Enter your choice: ")
        return choice
    
    def start(self) -> None:
        exitCondition = None
        while exitCondition != '0':
            choice = self.askChoice()
            if choice == '1':
                self.__addStudent()
            elif choice == '2':
                self.__viewRecords()
            elif choice == '3':
                self.__updateRecords()
            elif choice == '4':
                self.__addCourse()
            elif choice == '5':
                self.__viewCourses()
            elif choice == '6':
                self.__enroll()
            elif choice == '7':
                self.__studentEnroll()
            elif choice == '0':
                break
            else:
                print("Unkown option")
            print("")
        return None
    
    def __addStudent(self) -> None:
        cursor = DB_CONN.cursor()
        sql_statment = "INSERT INTO students (name, age, email) VALUES(?, ?, ?)"
        record_data = self.__askStudentDetails()
        cursor.execute(sql_statment, record_data)
        DB_CONN.commit()
        cursor.close()

    def __askStudentDetails(self) -> tuple:
        print("Insert students' info")
        name = input("Name: ")
        email = input("Email: ")
        age = int(input("Age: "))
        student_data = (name, email, age)
        return student_data
    
    def __viewRecords(self) -> None:
        students = self.__getStudents()
        print("Students: ")
        for student in students:
            print(f"Student Id: {student[0]} - Name: {student[1]}, age: {student[2]}, Email:{student[3]}")
        return None

    def __getStudents(self) -> list:
        cursor = DB_CONN.cursor()
        sql_statment = "SELECT * FROM students"
        cursor.execute(sql_statment)
        records = cursor.fetchall()
        DB_CONN.commit()
        cursor.close()
        return records
    
    def __updateRecords(self) -> None:
        student_id = input("Enter the ID of the student to update: ")
        cursor = DB_CONN.cursor()
        sql_statement = "SELECT * FROM students WHERE id = ?"
        cursor.execute(sql_statement, (student_id,))
        student_data = cursor.fetchone()

        if student_data is not None:
            print(f"Current record: {student_data}")
            new_name = input("Enter new name (or leave blank to keep the current name): ")
            new_email = input("Enter new email (or leave blank to keep the current email): ")
            new_age = int(input("Enter new age (or leave blank to keep the current age): "))

            if len(new_name.strip()) > 0:
                student_data = student_data[:1] + (new_name,) + student_data[2:]
            if len(new_email.strip()) > 0:
                student_data = student_data[:3] + (new_email,) + student_data[4:]
            if len(new_age.strip()) > 0:
                student_data = student_data[:2] + (new_age,) + student_data[3:]


            sql_statement = "UPDATE students SET name = ?, age = ?, email = ? WHERE id = ?"
            cursor.execute(sql_statement, (*student_data[1:], student_data[0]))
            DB_CONN.commit()
            print(f"Record updated: {student_data}")
        else:
            print(f"No record found with ID {student_id}")

        cursor.close()
        return None

    def __addCourse(self) -> None:
        cursor = DB_CONN.cursor()
        sql_statment = "INSERT INTO courses (name, teacher_id) VALUES (?, ?)"
        record_data = self.__askCourseDetail()
        cursor.execute(sql_statment, record_data)
        DB_CONN.commit()
        cursor.close()
        return None

    def __askCourseDetail(self) -> tuple:
        print("Insert course details")
        name = input("Course name: ")
        teacher_id = int(input("Teacher's ID: "))
        course_data = (name, teacher_id)
        return course_data
    
    def __viewCourses(self) -> None:
        courses = self.__getCourse()
        print("Course: ")
        for course in courses:
            print(f"Course: {course[0]} - Name: {course[1]} Teacher ID: {course[2]}")
        return None
    
    def __getCourse(self) -> list:
        cursor = DB_CONN.cursor()
        sql_statment = "SELECT * FROM courses"
        cursor.execute(sql_statment)
        records = cursor.fetchall()
        DB_CONN.commit()
        cursor.close()
        return records
    
    def __enroll(self) -> None:
        # Get student ID
        student_id = input("Enter student ID: ")
        student = self.__getStudentById(student_id)
        if student is None:
            print("Student not found")
            return None

        # Get course ID
        course_id = input("Enter course ID: ")
        course = self.__getCourseById(course_id)
        if course is None:
            print("Course not found")
            return None

        # Check if the student is already enrolled in the course
        if self.__isEnrolled(student_id, course_id):
            print("Student already enrolled in the course")
            return None

        # Enroll the student in the course
        cursor = DB_CONN.cursor()
        sql_statement = "INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)"
        cursor.execute(sql_statement, (student_id, course_id))
        DB_CONN.commit()
        cursor.close()

        print(f"Student {student[1]} has been enrolled in course {course[1]}")
        return None
    
    def __getStudentById(self, student_id: int) -> tuple:
        cursor = DB_CONN.cursor()
        sql_statement = "SELECT * FROM students WHERE id = ?"
        cursor.execute(sql_statement, (student_id,))
        record = cursor.fetchone()
        DB_CONN.commit()
        cursor.close()
        return record
    
    def __getCourseById(self, course_id: int) -> tuple:
        cursor = DB_CONN.cursor()
        sql_statement = "SELECT * FROM courses WHERE id  = ?"
        cursor.execute(sql_statement, (course_id,))
        course = cursor.fetchone()
        DB_CONN.commit()
        cursor.close()
        return course
    
    def __isEnrolled(self, student_id: int, course_id: int) -> bool:
        cursor = DB_CONN.cursor()
        sql_statement = "SELECT * FROM enrollments WHERE student_id = ? AND course_id = ?"
        cursor.execute(sql_statement, (student_id, course_id))
        record = cursor.fetchone()
        cursor.close()
        return record is not None

