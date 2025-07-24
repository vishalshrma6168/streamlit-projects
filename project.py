import mysql.connector
from tkinter import *
from tkinter import messagebox

# ---------- Database Functions ----------
def connect_db():
    return mysql.connector.connect(
        host="localhost",       # or "127.0.0.1"
        user="root",            # your MySQL username
        password="hp22d6168",            # your MySQL password
        database="contactbook"  # the database you created
    )

def insert_contact(name, phone, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contact (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
    conn.commit()
    conn.close()

def view_contacts():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact")
    rows = cursor.fetchall()
    conn.close()
    return rows

def delete_contact(contact_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contact WHERE id = %s", (contact_id,))
    conn.commit()
    conn.close()

def update_contact(contact_id, name, phone, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE contact SET name=%s, phone=%s, email=%s WHERE id=%s", (name, phone, email, contact_id))
    conn.commit()
    conn.close()

# ---------- GUI Functions ----------
def add_contact():
    if name_var.get() and phone_var.get():
        insert_contact(name_var.get(), phone_var.get(), email_var.get())
        messagebox.showinfo("Success", "Contact added!")
        view_all()
    else:
        messagebox.showwarning("Input Error", "Name and Phone are required")

def view_all():
    listbox.delete(0, END)
    for row in view_contacts():
        listbox.insert(END, row)

def on_select(event):
    global selected_contact
    try:
        index = listbox.curselection()[0]
        selected_contact = listbox.get(index)
        name_entry.delete(0, END)
        name_entry.insert(END, selected_contact[1])
        phone_entry.delete(0, END)
        phone_entry.insert(END, selected_contact[2])
        email_entry.delete(0, END)
        email_entry.insert(END, selected_contact[3])
    except IndexError:
        pass

def delete_selected():
    try:
        delete_contact(selected_contact[0])
        messagebox.showinfo("Deleted", "Contact deleted")
        view_all()
    except:
        messagebox.showerror("Error", "No contact selected")

def update_selected():
    try:
        update_contact(selected_contact[0], name_var.get(), phone_var.get(), email_var.get())
        messagebox.showinfo("Updated", "Contact updated")
        view_all()
    except:
        messagebox.showerror("Error", "No contact selected")

# ---------- GUI Setup ----------
root = Tk()
root.title("Contact Book (MySQL)")

# Entry fields
Label(root, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_var = StringVar()
name_entry = Entry(root, textvariable=name_var)
name_entry.grid(row=0, column=1)

Label(root, text="Phone").grid(row=1, column=0, padx=5)
phone_var = StringVar()
phone_entry = Entry(root, textvariable=phone_var)
phone_entry.grid(row=1, column=1)

Label(root, text="Email").grid(row=2, column=0, padx=5)
email_var = StringVar()
email_entry = Entry(root, textvariable=email_var)
email_entry.grid(row=2, column=1)

# Buttons
Button(root, text="Add Contact", command=add_contact).grid(row=3, column=0, pady=5)
Button(root, text="Update Contact", command=update_selected).grid(row=3, column=1)
Button(root, text="Delete Contact", command=delete_selected).grid(row=4, column=0)
Button(root, text="View All", command=view_all).grid(row=4, column=1)

# Listbox
listbox = Listbox(root, width=50)
listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10)
listbox.bind('<<ListboxSelect>>', on_select)

# Run
view_all()
root.mainloop()