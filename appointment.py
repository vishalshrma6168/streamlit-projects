import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox
from datetime import datetime

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hp22d6168 ",  # Change this!
    database="appointment_db"
)
cursor = conn.cursor()

# Functions
def add_client():
    name = client_name_var.get()
    phone = client_phone_var.get()
    email = client_email_var.get()

    if not name or not phone or not email:
        messagebox.showwarning("Input error", "All client fields are required")
        return

    cursor.execute(
        "INSERT INTO clients (name, phone, email) VALUES (%s, %s, %s)",
        (name, phone, email)
    )
    conn.commit()
    messagebox.showinfo("Success", "Client added successfully!")
    clear_client_inputs()
    load_clients()

def load_clients():
    client_combo['values'] = []
    cursor.execute("SELECT id, name FROM clients")
    clients = cursor.fetchall()
    client_combo['values'] = [f"{cid} - {cname}" for cid, cname in clients]

def clear_client_inputs():
    client_name_var.set("")
    client_phone_var.set("")
    client_email_var.set("")

def add_appointment():
    client = client_combo.get()
    appt_date = appt_date_var.get()
    appt_time = appt_time_var.get()
    service = service_var.get()

    if not client or not appt_date or not appt_time or not service:
        messagebox.showwarning("Input error", "All appointment fields are required")
        return

    try:
        client_id = int(client.split(" - ")[0])
    except:
        messagebox.showwarning("Input error", "Select a valid client")
        return

    try:
        datetime.strptime(appt_date, '%Y-%m-%d')
        datetime.strptime(appt_time, '%H:%M')
    except ValueError:
        messagebox.showwarning("Input error", "Date must be YYYY-MM-DD and time HH:MM")
        return

    cursor.execute(
        "INSERT INTO appointments (client_id, appointment_date, appointment_time, service_type) VALUES (%s, %s, %s, %s)",
        (client_id, appt_date, appt_time, service)
    )
    conn.commit()
    messagebox.showinfo("Success", "Appointment added successfully!")
    clear_appointment_inputs()
    load_appointments()

def load_appointments():
    for row in appointment_tree.get_children():
        appointment_tree.delete(row)
    cursor.execute("""
        SELECT a.id, c.name, a.appointment_date, a.appointment_time, a.service_type
        FROM appointments a
        JOIN clients c ON a.client_id = c.id
        ORDER BY a.appointment_date, a.appointment_time
    """)
    for appt in cursor.fetchall():
        appointment_tree.insert("", END, values=appt)

def clear_appointment_inputs():
    client_combo.set("")
    appt_date_var.set("")
    appt_time_var.set("")
    service_var.set("")

def delete_appointment():
    selected = appointment_tree.focus()
    if not selected:
        messagebox.showwarning("Select appointment", "Please select an appointment to delete")
        return
    appt_id = appointment_tree.item(selected, "values")[0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this appointment?")
    if confirm:
        cursor.execute("DELETE FROM appointments WHERE id=%s", (appt_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Appointment deleted successfully!")
        load_appointments()

# Tkinter UI
root = Tk()
root.title("Appointment Scheduling System")
root.geometry("700x500")

# Variables
client_name_var = StringVar()
client_phone_var = StringVar()
client_email_var = StringVar()

appt_date_var = StringVar()
appt_time_var = StringVar()
service_var = StringVar()
client_combo = ttk.Combobox(root, width=30)

# Client Frame
client_frame = LabelFrame(root, text="Add New Client")
client_frame.place(x=20, y=20, width=320, height=150)

Label(client_frame, text="Name").grid(row=0, column=0, padx=10, pady=5)
Entry(client_frame, textvariable=client_name_var).grid(row=0, column=1, padx=10, pady=5)

Label(client_frame, text="Phone").grid(row=1, column=0, padx=10, pady=5)
Entry(client_frame, textvariable=client_phone_var).grid(row=1, column=1, padx=10, pady=5)

Label(client_frame, text="Email").grid(row=2, column=0, padx=10, pady=5)
Entry(client_frame, textvariable=client_email_var).grid(row=2, column=1, padx=10, pady=5)

Button(client_frame, text="Add Client", command=add_client).grid(row=3, column=0, columnspan=2, pady=10)

# Appointment Frame
appt_frame = LabelFrame(root, text="Schedule Appointment")
appt_frame.place(x=360, y=20, width=320, height=200)

Label(appt_frame, text="Client").grid(row=0, column=0, padx=10, pady=5)
client_combo.grid(row=0, column=1, padx=10, pady=5)

Label(appt_frame, text="Date (YYYY-MM-DD)").grid(row=1, column=0, padx=10, pady=5)
Entry(appt_frame, textvariable=appt_date_var).grid(row=1, column=1, padx=10, pady=5)

Label(appt_frame, text="Time (HH:MM)").grid(row=2, column=0, padx=10, pady=5)
Entry(appt_frame, textvariable=appt_time_var).grid(row=2, column=1, padx=10, pady=5)

Label(appt_frame, text="Service Type").grid(row=3, column=0, padx=10, pady=5)
Entry(appt_frame, textvariable=service_var).grid(row=3, column=1, padx=10, pady=5)

Button(appt_frame, text="Add Appointment", command=add_appointment).grid(row=4, column=0, columnspan=2, pady=10)

# Appointment List
appointment_tree = ttk.Treeview(root, columns=("ID", "Client", "Date", "Time", "Service"), show="headings")
appointment_tree.heading("ID", text="ID")
appointment_tree.heading("Client", text="Client")
appointment_tree.heading("Date", text="Date")
appointment_tree.heading("Time", text="Time")
appointment_tree.heading("Service", text="Service")

appointment_tree.column("ID", width=40)
appointment_tree.column("Client", width=140)
appointment_tree.column("Date", width=100)
appointment_tree.column("Time", width=80)
appointment_tree.column("Service", width=150)

appointment_tree.place(x=20, y=200, width=660, height=280)

Button(root, text="Delete Appointment", command=delete_appointment).place(x=280, y=490)

# Load clients and appointments on start
load_clients()
load_appointments()

root.mainloop()
