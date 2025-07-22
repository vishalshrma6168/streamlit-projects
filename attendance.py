import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hp22d6168",  # Change this!
    database="attendance_db"
)
cursor = conn.cursor()

# Functions
def add_employee():
    name = name_var.get()
    department = department_var.get()
    email = email_var.get()

    if not name or not department or not email:
        messagebox.showwarning("Input error", "All fields are required")
        return

    cursor.execute(
        "INSERT INTO employees (name, department, email) VALUES (%s, %s, %s)",
        (name, department, email)
    )
    conn.commit()
    messagebox.showinfo("Success", "Employee added successfully!")
    clear_employee_inputs()
    load_employees()

def load_employees():
    for row in employee_tree.get_children():
        employee_tree.delete(row)
    cursor.execute("SELECT * FROM employees")
    for emp in cursor.fetchall():
        employee_tree.insert("", END, values=emp)

def clear_employee_inputs():
    name_var.set("")
    department_var.set("")
    email_var.set("")

def select_employee(event):
    selected = employee_tree.focus()
    if selected:
        values = employee_tree.item(selected, "values")
        name_var.set(values[1])
        department_var.set(values[2])
        email_var.set(values[3])

def mark_attendance():
    selected = employee_tree.focus()
    if not selected:
        messagebox.showwarning("Select employee", "Please select an employee to mark attendance")
        return
    
    emp_id = employee_tree.item(selected, "values")[0]
    status = attendance_status.get()
    today = date.today()

    # Check if attendance already marked today
    cursor.execute(
        "SELECT * FROM attendance WHERE employee_id=%s AND date=%s",
        (emp_id, today)
    )
    if cursor.fetchone():
        messagebox.showwarning("Already marked", "Attendance already marked for today")
        return

    cursor.execute(
        "INSERT INTO attendance (employee_id, date, status) VALUES (%s, %s, %s)",
        (emp_id, today, status)
    )
    conn.commit()
    messagebox.showinfo("Success", "Attendance marked successfully!")
    load_attendance()

def load_attendance():
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)
    cursor.execute("""
        SELECT a.id, e.name, a.date, a.status
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        ORDER BY a.date DESC
    """)
    for record in cursor.fetchall():
        attendance_tree.insert("", END, values=record)

def filter_attendance():
    keyword = search_var.get()
    query = """
        SELECT a.id, e.name, a.date, a.status
        FROM attendance a
        JOIN employees e ON a.employee_id = e.id
        WHERE e.name LIKE %s OR e.department LIKE %s
        ORDER BY a.date DESC
    """
    like_keyword = f"%{keyword}%"
    cursor.execute(query, (like_keyword, like_keyword))
    records = cursor.fetchall()
    for row in attendance_tree.get_children():
        attendance_tree.delete(row)
    for rec in records:
        attendance_tree.insert("", END, values=rec)

# Tkinter UI
root = Tk()
root.title("Employee Attendance System")
root.geometry("850x600")

# Variables
name_var = StringVar()
department_var = StringVar()
email_var = StringVar()
attendance_status = StringVar(value="Present")
search_var = StringVar()

# Employee Frame
emp_frame = LabelFrame(root, text="Employee Details")
emp_frame.place(x=20, y=20, width=400, height=180)

Label(emp_frame, text="Name").grid(row=0, column=0, padx=10, pady=10)
Entry(emp_frame, textvariable=name_var).grid(row=0, column=1, padx=10, pady=10)

Label(emp_frame, text="Department").grid(row=1, column=0, padx=10, pady=10)
Entry(emp_frame, textvariable=department_var).grid(row=1, column=1, padx=10, pady=10)

Label(emp_frame, text="Email").grid(row=2, column=0, padx=10, pady=10)
Entry(emp_frame, textvariable=email_var).grid(row=2, column=1, padx=10, pady=10)

Button(emp_frame, text="Add Employee", command=add_employee, width=15).grid(row=3, column=0, columnspan=2, pady=10)

# Employee List
employee_tree = ttk.Treeview(root, columns=("ID", "Name", "Department", "Email"), show="headings")
employee_tree.heading("ID", text="ID")
employee_tree.heading("Name", text="Name")
employee_tree.heading("Department", text="Department")
employee_tree.heading("Email", text="Email")
employee_tree.column("ID", width=40)
employee_tree.column("Name", width=120)
employee_tree.column("Department", width=100)
employee_tree.column("Email", width=140)
employee_tree.place(x=20, y=210, width=400, height=350)
employee_tree.bind("<<TreeviewSelect>>", select_employee)

# Attendance Frame
att_frame = LabelFrame(root, text="Mark Attendance")
att_frame.place(x=450, y=20, width=380, height=120)

Radiobutton(att_frame, text="Present", variable=attendance_status, value="Present").pack(anchor=W, padx=20, pady=5)
Radiobutton(att_frame, text="Absent", variable=attendance_status, value="Absent").pack(anchor=W, padx=20)

Button(att_frame, text="Mark Attendance", command=mark_attendance, width=20).pack(pady=10)

# Attendance List
Label(root, text="Attendance Records").place(x=450, y=160)
search_entry = Entry(root, textvariable=search_var)
search_entry.place(x=450, y=185, width=250)
Button(root, text="Search", command=filter_attendance).place(x=710, y=180)

attendance_tree = ttk.Treeview(root, columns=("ID", "Employee", "Date", "Status"), show="headings")
attendance_tree.heading("ID", text="ID")
attendance_tree.heading("Employee", text="Employee")
attendance_tree.heading("Date", text="Date")
attendance_tree.heading("Status", text="Status")
attendance_tree.column("ID", width=40)
attendance_tree.column("Employee", width=120)
attendance_tree.column("Date", width=100)
attendance_tree.column("Status", width=80)
attendance_tree.place(x=450, y=220, width=380, height=340)

# Load initial data
load_employees()
load_attendance()

root.mainloop()
