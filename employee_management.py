import mysql.connector
from tabulate import tabulate

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="type your mysql password",
        database="emp"
    )

# Function to check if an employee exists
def check_employee(cursor, employee_id):
    try:
        sql = 'SELECT * FROM employees WHERE id=%s'
        cursor.execute(sql, (employee_id,))
        cursor.fetchall()  # Fetch all results to clear the buffer
        return cursor.rowcount == 1
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False

# Function to add an employee
def add_employee(cursor, conn):
    Id = input("Enter Employee Id: ")
    if check_employee(cursor, Id):
        print("Employee already exists. Please try again.")
        return
    
    Name = input("Enter Employee Name: ")
    Post = input("Enter Employee Post: ")
    Salary = float(input("Enter Employee Salary: "))  # Change to float or Decimal
    
    sql = 'INSERT INTO employees (id, name, position, salary) VALUES (%s, %s, %s, %s)'
    data = (Id, Name, Post, Salary)
    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Employee Added Successfully")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()
    except ValueError as err:
        print(f"Value error: {err}")

# Function to remove an employee
def remove_employee(cursor, conn):
    Id = input("Enter Employee Id: ")
    if not check_employee(cursor, Id):
        print("Employee does not exist. Please try again.")
        return
    
    sql = 'DELETE FROM employees WHERE id=%s'
    data = (Id,)
    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Employee Removed Successfully")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()

# Function to promote or demote an employee
def promote_or_demote_employee(cursor, conn):
    Id = input("Enter Employee's Id: ")
    if not check_employee(cursor, Id):
        print("Employee does not exist. Please try again.")
        return
    
    try:
        action = input("Enter 'increase' to increase salary or 'decrease' to decrease salary: ").strip().lower()
        if action not in ['increase', 'decrease']:
            print("Invalid action. Please enter 'increase' or 'decrease'.")
            return
        
        Amount = float(input("Enter the amount to change the Salary by: "))
        sql_select = 'SELECT salary FROM employees WHERE id=%s'
        cursor.execute(sql_select, (Id,))
        current_salary = cursor.fetchone()[0]
        current_salary = float(current_salary)  # Ensure current_salary is float
        
        if action == 'increase':
            new_salary = current_salary + Amount
        elif action == 'decrease':
            new_salary = current_salary - Amount
        
        sql_update = 'UPDATE employees SET salary=%s WHERE id=%s'
        cursor.execute(sql_update, (new_salary, Id))
        conn.commit()
        print(f"Employee's salary has been {action}d successfully.")

    except (ValueError, mysql.connector.Error) as e:
        print(f"Error: {e}")
        conn.rollback()

# Function to update employee details
def update_employee(cursor, conn):
    Id = input("Enter Employee Id: ")
    if not check_employee(cursor, Id):
        print("Employee does not exist. Please try again.")
        return
    
    print("Which detail do you want to update?")
    print("1. Name")
    print("2. Position")
    print("3. Salary")
    choice = input("Enter your choice (1/2/3): ")

    if choice not in ['1', '2', '3']:
        print("Invalid choice. Please try again.")
        return

    new_value = input("Enter new value: ")
    
    if choice == '1':
        sql_update = 'UPDATE employees SET name=%s WHERE id=%s'
        data = (new_value, Id)
    elif choice == '2':
        sql_update = 'UPDATE employees SET position=%s WHERE id=%s'
        data = (new_value, Id)
    elif choice == '3':
        try:
            new_salary = float(new_value)
            sql_update = 'UPDATE employees SET salary=%s WHERE id=%s'
            data = (new_salary, Id)
        except ValueError:
            print("Invalid salary amount. Please enter a valid number.")
            return

    try:
        cursor.execute(sql_update, data)
        conn.commit()
        print("Employee details updated successfully.")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        conn.rollback()

# Function to generate and display employee salary
def salary_generator(cursor):
    try:
        sql = 'SELECT name, salary FROM employees'
        cursor.execute(sql)
        employees = cursor.fetchall()
        if not employees:
            print("No employees found.")
        for employee in employees:
            print(f"Employee Name: {employee[0]}, Salary: {employee[1]}")
    except mysql.connector.Error as err:
        print(f"Database error: {err}")

# Function to display all employees
def display_employees(cursor):
    try:
        sql = 'SELECT * FROM employees'
        cursor.execute(sql)
        employees = cursor.fetchall()
        if not employees:
            print("No employees found.")
        headers = ["Employee Id", "Employee Name", "Employee Post", "Employee Salary"]
        table = tabulate(employees, headers=headers, tablefmt='grid')
        
        print("Employee List: ")
        print(table)
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
