import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hp22d6168",  # change this!
    database="hospital_db"
)
cursor = conn.cursor()

# Functions
def add_patient():
    name = name_var.get()
    age = age_var.get()
    gender = gender_var.get()
    disease = disease_var.get()
    contact = contact_var.get()

    if not name or not age or not gender or not disease or not contact:
        messagebox.showwarning("Input error", "All fields are required")
        return
    
    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Input error", "Age must be an integer")
        return

    cursor.execute(
        "INSERT INTO patients (name, age, gender, disease, contact) VALUES (%s, %s, %s, %s, %s)",
        (name, age, gender, disease, contact)
    )
    conn.commit()
    messagebox.showinfo("Success", "Patient added successfully!")
    clear_inputs()
    load_patients()

def load_patients():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM patients")
    for patient in cursor.fetchall():
        tree.insert("", END, values=patient)

def clear_inputs():
    name_var.set("")
    age_var.set("")
    gender_var.set("")
    disease_var.set("")
    contact_var.set("")

def select_patient(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        clear_inputs()
        name_var.set(values[1])
        age_var.set(values[2])
        gender_var.set(values[3])
        disease_var.set(values[4])
        contact_var.set(values[5])

def update_patient():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select patient", "Please select a patient to update")
        return
    
    patient_id = tree.item(selected, "values")[0]
    name = name_var.get()
    age = age_var.get()
    gender = gender_var.get()
    disease = disease_var.get()
    contact = contact_var.get()

    if not name or not age or not gender or not disease or not contact:
        messagebox.showwarning("Input error", "All fields are required")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showwarning("Input error", "Age must be an integer")
        return

    cursor.execute(
        "UPDATE patients SET name=%s, age=%s, gender=%s, disease=%s, contact=%s WHERE id=%s",
        (name, age, gender, disease, contact, patient_id)
    )
    conn.commit()
    messagebox.showinfo("Success", "Patient updated successfully!")
    clear_inputs()
    load_patients()

def delete_patient():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select patient", "Please select a patient to delete")
        return
    patient_id = tree.item(selected, "values")[0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this patient?")
    if confirm:
        cursor.execute("DELETE FROM patients WHERE id=%s", (patient_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Patient deleted successfully!")
        clear_inputs()
        load_patients()

def search_patients():
    keyword = search_var.get()
    query = "SELECT * FROM patients WHERE name LIKE %s OR disease LIKE %s"
    like_keyword = f"%{keyword}%"
    cursor.execute(query, (like_keyword, like_keyword))
    results = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for patient in results:
        tree.insert("", END, values=patient)

# Tkinter UI setup
root = Tk()
root.title("Hospital Patient Management System")
root.geometry("750x500")

# Variables
name_var = StringVar()
age_var = StringVar()
gender_var = StringVar()
disease_var = StringVar()
contact_var = StringVar()
search_var = StringVar()

# Widgets
Label(root, text="Name").place(x=20, y=20)
Entry(root, textvariable=name_var).place(x=100, y=20)

Label(root, text="Age").place(x=20, y=60)
Entry(root, textvariable=age_var).place(x=100, y=60)

Label(root, text="Gender").place(x=20, y=100)
Entry(root, textvariable=gender_var).place(x=100, y=100)

Label(root, text="Disease").place(x=20, y=140)
Entry(root, textvariable=disease_var).place(x=100, y=140)

Label(root, text="Contact").place(x=20, y=180)
Entry(root, textvariable=contact_var).place(x=100, y=180)

Button(root, text="Add Patient", command=add_patient, width=15).place(x=20, y=220)
Button(root, text="Update Patient", command=update_patient, width=15).place(x=150, y=220)
Button(root, text="Delete Patient", command=delete_patient, width=15).place(x=280, y=220)

Label(root, text="Search").place(x=420, y=20)
Entry(root, textvariable=search_var).place(x=480, y=20)
Button(root, text="Search", command=search_patients).place(x=620, y=16)

# Treeview
columns = ("ID", "Name", "Age", "Gender", "Disease", "Contact")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    if col == "Name" or col == "Disease":
        tree.column(col, width=140)
    else:
        tree.column(col, width=80)

tree.place(x=20, y=270, width=700, height=200)
tree.bind("<ButtonRelease-1>", select_patient)

# Load patients initially
load_patients()

root.mainloop()
