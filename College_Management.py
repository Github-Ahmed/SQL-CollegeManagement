import mysql.connector as mysql

db = mysql.connect(host="localhost", user="root", password="", database="college")
command_handler = db.cursor(buffered=True)

def admin_session():
    print("\nLogin Success, Welcome admin\n")

    while 1:
        print("\nAdmin Menu: ")
        print("1. Register new student\
            2. Register new Teacher\
            3. Delete Existing Student\
            4. Delete Existing Teacher\
            5. Logout\n")

        user_option = input(str("Your option: "))
        if user_option == '1':
            print("\nRegister New Student:")
            username = input(str('Student username: '))
            password = input((str("Student password: ")))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users(username, password, privilege) VALUES(%s,%s, 'student')", query_vals)
            db.commit()
            print(username + ' has been registered as a student')

        elif user_option == '2':
            print("\nRegister New Teacher:")
            username = input(str('Teacher username: '))
            password = input((str("Teacher password: ")))
            query_vals = (username, password)
            command_handler.execute("INSERT INTO users(username, password, privilege) VALUES(%s,%s, 'teacher')", query_vals)
            db.commit()
            print(username + ' has been registered as a teacher')

        elif user_option == '3':
            print("\nDelete an existing student account: ")
            student_name = input(str("Enter the student name to be deleted: "))
            query_vals = (student_name, "student")
            command_handler.execute("DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()

            if command_handler.rowcount < 1: 
                print("\nUser not found....")
            else: 
                print(student_name + ' has been deleted from the database.')

        elif user_option == '4':
            print("\nDelete an existing teacher account: ")
            teacher_name = input(str("Enter the teacher name to be deleted: "))
            query_vals = (teacher_name, "teacher")
            command_handler.execute(
                "DELETE FROM users WHERE username = %s AND privilege = %s", query_vals)
            db.commit()

            if command_handler.rowcount < 1:
                print("\nUser not found....")
            else:
                print(teacher_name + ' has been deleted from the database.')
        
        elif user_option == '5':
            break

        else:
            print("\nPlease enter a valid option. ")

def auth_admin():
    print("\nAdmin login: \n")
    username = input(str("Enter Username: "))
    password = input(str("Enter Password: "))

    if username == 'admin':
        if password == 'password':
            admin_session()
        
        else:
            print("Incorrect password!")
    else:
        print("Login details not recognized")


def teacher_session():
    print("\nWelcome teacher.\n")
    while 1:
        print("\nTeacher Menu: ")
        print("1. Mark student's register\n2. View Register\n3. Logout\n")

        user_option = input(str("Your option: "))
        if user_option == '1':
            print("\nMark student's register: ")
            command_handler.execute("SELECT username FROM users WHERE privilege = 'student'")
            records = command_handler.fetchall()
            date = input(str("Date: DD/MM/YYYY: "))

            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")

                # Present | Absent | Late
                status = input(str("Status for ") + str(record) + " P/A/L: ")
                query_vals = (str(record), date, status)
                command_handler.execute("INSERT INTO attendance(username, date, status) VALUES (%s, %s, %s)", query_vals)
                db.commit()
                print(record + " Marked as " + status + "\n")

        elif user_option == "2":
            print("\nView student's register: \n")
            date = input(str("Enter a date (DD/MM/YYYY) you want to see register of\nOr press 0 to view all\n: "))
            query_vals = (date,)
            if date != "0":
                command_handler.execute("SELECT date, username, status FROM attendance WHERE date = %s", query_vals)
                records = command_handler.fetchall()
                for record in records: 
                    print('')
                    print(record)

            elif date == "0":
                print("Displaying all the complete register: ")
                command_handler.execute("SELECT date, username, status FROM attendance ORDER BY date DESC")
                records = command_handler.fetchall()
                for record in records:
                    print('')
                    print(record)

            else:
                print("\nEnter a valid option: ")
      
        elif user_option == "3":
            break

        else:
            print("\nPlease enter a valid option!\n")

def auth_teacher():
    print("\nTeacher login: \n")

    username = input(str("Enter your username: "))
    password = input(str("Enter your password "))
    query_vals = (username, password)
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = 'teacher'", query_vals)

    if command_handler.rowcount <= 0: 
        print("\nLogin not recognized")
    else: 
        teacher_session()

def student_session(username):
    print("\nWelcome student. \n")
    while 1: 
        print("\nStudent's Menu: ")
        print("1. View register\n2. Download register\n3. Logout\n")

        user_option = input(str("Your option: "))
        if user_option == '1':
            username = (username,)
            print("\nHere is your register: ")
            command_handler.execute("SELECT date, username, status FROM attendance ORDER BY date DESC WHERE username = %s", username)
            records = command_handler.fetchall()
            for record in records:
                print('')
                print(record)

        elif user_option == '2':
            print("Downloading register: ")
            username = (username,)
            command_handler.execute(
                "SELECT date, username, status FROM attendance WHERE username = %s ORDER BY date DESC", username)
            records = command_handler.fetchall()
            
            for record in records:
                with open("/Users/Ahmed/PythonProjects/MySQL learning/register.txt", "w") as file:
                    var = '\n'
                    file.write(var)
                    file.write((str(records)))
                file.close()
            print("All records have been saved.")

        elif user_option == "3":
            break

        else: 
            print("\nEnter a valid option.\n")

def auth_student():
    print("\nStudent login: \n")

    username = input(str("Enter your username: "))
    password = input(str("Enter your password "))
    query_vals = (username, password, "student")
    command_handler.execute("SELECT * FROM users WHERE username = %s AND password = %s AND privilege = %s", query_vals)

    if command_handler.rowcount <= 0:
        print("\nLogin not recognized")
    else:
        student_session(username)


def main():
    while 1:
        print("\nWelcome to the college system: \n1. Student login.\n2. Teacher login\n3. Admin login\n4. Exit")
        user_input = input(str("Enter your option: "))

        if user_input == "1":
            auth_student()
        elif user_input == "2":
            auth_teacher()
        elif user_input == "3": 
            auth_admin()
        elif user_input == "4":
            break
        else:
            print("\nEnter valid option")

main()

# ----------------------------------------------------------------------------------------------------------------------------------------------------
