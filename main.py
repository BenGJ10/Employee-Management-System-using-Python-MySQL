import employee_management as em

import mysql.connector
from employee_management import get_connection, add_employee, remove_employee, promote_or_demote_employee, update_employee, salary_generator, display_employees

def menu():
    conn = get_connection()
    cursor = conn.cursor()
    
    while True:
        print("\nWelcome to Employee Management System")
        print("Press:")
        print("1 to Add Employee")
        print("2 to Remove Employee")
        print("3 to Promote/ Demote Employee")
        print("4 to Update Employee Details")
        print("5 to Display Employees")
        print("6 to Generate Salary Report")
        print("7 to Exit")
        
        ch = input("Enter your Choice: ")

        try:
            if ch == '1':
                print("\n")
                add_employee(cursor, conn)
            elif ch == '2':
                print("\n")
                remove_employee(cursor, conn)
            elif ch == '3':
                print("\n")
                promote_or_demote_employee(cursor, conn)
            elif ch == '4':
                print("\n")
                update_employee(cursor, conn)
            elif ch == '5':
                print("\n")
                display_employees(cursor)
            elif ch == '6':
                print("\n")
                salary_generator(cursor)
            elif ch == '7':
                print("\n")
                print("Exiting Employee Management System... GoodBye!")
                break
            else:
                print("Invalid Choice! Please try again.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    menu()
