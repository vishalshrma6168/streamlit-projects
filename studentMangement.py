import mysql.connector
from tkinter import *
from tkinter import messagebox

# ---------- Database Operations ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # your username
        password="hp22d6168",       # your password
        database="studentdb"
    )

def insert_student(name, roll_no, s_class, section):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO student (name, roll_no, class, section) VALUES (%s, %s, %s, %s)",
                (name, roll_no, s_class, section))
    conn.commit()
    conn.close()

def view_students():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_student(student_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=%s", (student_id,))
    conn.commit()
    conn.close()

def update_student(student_id, name, roll_no, s_class, section):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=%s, roll_no=%s, class=%s, section=%s WHERE id=%s",
                (name, roll_no, s_class, section, student_id))
    conn.commit()
    conn.close()

def search_students(keyword):
    conn = connect_db()
    cur = conn.cursor()
    query = "SELECT * FROM student WHERE name LIKE %s OR roll_no LIKE %s"
    cur.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
    rows = cur.fetchall()
    conn.close()
    return rows

# ---------- GUI Setup ----------
def add_student():
    if name_var.get() and roll_var.get():
        insert_student(name_var.get(), roll_var.get(), class_var.get(), section_var.get())
        messagebox.showinfo("Success", "Student added!")
        view_all()
    else:
        messagebox.showwarning("Missing Info", "Name and Roll No are required.")

def view_all():
    listbox.delete(0, END)
    for row in view_students():
        listbox.insert(END, row)

def on_select(event):
    global selected_student
    try:
        index = listbox.curselection()[0]
        selected_student = listbox.get(index)
        name_entry.delete(0, END)
        name_entry.insert(END, selected_student[1])
        roll_entry.delete(0, END)
        roll_entry.insert(END, selected_student[2])
        class_entry.delete(0, END)
        class_entry.insert(END, selected_student[3])
        section_entry.delete(0, END)
        section_entry.insert(END, selected_student[4])
    except IndexError:
        pass

def delete_selected():
    try:
        delete_student(selected_student[0])
        messagebox.showinfo("Deleted", "Student record deleted")
        view_all()
    except:
        messagebox.showerror("Error", "Please select a student")

def update_selected():
    try:
        update_student(selected_student[0], name_var.get(), roll_var.get(), class_var.get(), section_var.get())
        messagebox.showinfo("Updated", "Student record updated")
        view_all()
    except:
        messagebox.showerror("Error", "Please select a student")

def search_student():
    keyword = search_var.get()
    results = search_students(keyword)
    listbox.delete(0, END)
    for row in results:
        listbox.insert(END, row)

# ---------- GUI Layout ----------
root = Tk()
root.title("Student Management System")

# Entry Fields
Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_var = StringVar()
name_entry = Entry(root, textvariable=name_var)
name_entry.grid(row=0, column=1)

Label(root, text="Roll No").grid(row=1, column=0, padx=5)
roll_var = StringVar()
roll_entry = Entry(root, textvariable=roll_var)
roll_entry.grid(row=1, column=1)

Label(root, text="Class").grid(row=2, column=0, padx=5)
class_var = StringVar()
class_entry = Entry(root, textvariable=class_var)
class_entry.grid(row=2, column=1)

Label(root, text="Section").grid(row=3, column=0, padx=5)
section_var = StringVar()
section_entry = Entry(root, textvariable=section_var)
section_entry.grid(row=3, column=1)

# Buttons
Button(root, text="Add Student", width=15, command=add_student).grid(row=4, column=0, pady=10)
Button(root, text="Update", width=15, command=update_selected).grid(row=4, column=1)
Button(root, text="Delete", width=15, command=delete_selected).grid(row=5, column=0)
Button(root, text="View All", width=15, command=view_all).grid(row=5, column=1)

# Search Box
Label(root, text="Search").grid(row=6, column=0, pady=5)
search_var = StringVar()
Entry(root, textvariable=search_var).grid(row=6, column=1)
Button(root, text="Search", command=search_student).grid(row=7, column=0, columnspan=2, pady=5)

# Listbox
listbox = Listbox(root, width=60)
listbox.grid(row=8, column=0, columnspan=2, padx=10, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

view_all()
root.mainloop()
