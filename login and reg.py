import tkinter as tk
from tkinter import messagebox
import mysql.connector

# MySQL Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hp22d6168",  # use your MySQL password
    database="userdb"
)
cursor = conn.cursor()

# Register User
def register_user():
    name = entry_name.get()
    email = entry_email.get()
    password = entry_password.get()

    if not name or not email or not password:
        messagebox.showerror("Error", "All fields are required")
        return

    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, password))
        conn.commit()
        messagebox.showinfo("Success", "Registered Successfully")
    except mysql.connector.errors.IntegrityError:
        messagebox.showerror("Error", "Email already exists")

# Login User
def login_user():
    email = entry_email.get()
    password = entry_password.get()

    cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", 
                   (email, password))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Success", f"Welcome, {result[1]}!")
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# GUI Setup
root = tk.Tk()
root.title("Login & Register")
root.geometry("300x300")

tk.Label(root, text="Name").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Email").pack()
entry_email = tk.Entry(root)
entry_email.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Register", command=register_user).pack(pady=5)
tk.Button(root, text="Login", command=login_user).pack(pady=5)

root.mainloop()
