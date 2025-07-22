import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="hp22d6168",  # Change this!
    database="inventory_db"
)
cursor = conn.cursor()

# Functions
def add_product():
    name = name_var.get()
    category = category_var.get()
    quantity = quantity_var.get()
    price = price_var.get()

    if not name or not category or not quantity or not price:
        messagebox.showwarning("Input error", "All fields are required")
        return
    
    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        messagebox.showwarning("Input error", "Quantity must be integer and price must be number")
        return
    
    cursor.execute(
        "INSERT INTO products (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
        (name, category, quantity, price)
    )
    conn.commit()
    messagebox.showinfo("Success", "Product added successfully!")
    clear_inputs()
    load_products()

def load_products():
    for row in tree.get_children():
        tree.delete(row)
    cursor.execute("SELECT * FROM products")
    for product in cursor.fetchall():
        tree.insert("", END, values=product)

def clear_inputs():
    name_var.set("")
    category_var.set("")
    quantity_var.set("")
    price_var.set("")

def select_product(event):
    selected = tree.focus()
    if selected:
        values = tree.item(selected, "values")
        clear_inputs()
        name_var.set(values[1])
        category_var.set(values[2])
        quantity_var.set(values[3])
        price_var.set(values[4])

def update_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select product", "Please select a product to update")
        return
    
    product_id = tree.item(selected, "values")[0]
    name = name_var.get()
    category = category_var.get()
    quantity = quantity_var.get()
    price = price_var.get()

    if not name or not category or not quantity or not price:
        messagebox.showwarning("Input error", "All fields are required")
        return
    
    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        messagebox.showwarning("Input error", "Quantity must be integer and price must be number")
        return

    cursor.execute(
        "UPDATE products SET name=%s, category=%s, quantity=%s, price=%s WHERE id=%s",
        (name, category, quantity, price, product_id)
    )
    conn.commit()
    messagebox.showinfo("Success", "Product updated successfully!")
    clear_inputs()
    load_products()

def delete_product():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Select product", "Please select a product to delete")
        return
    product_id = tree.item(selected, "values")[0]
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this product?")
    if confirm:
        cursor.execute("DELETE FROM products WHERE id=%s", (product_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Product deleted successfully!")
        clear_inputs()
        load_products()

def search_products():
    keyword = search_var.get()
    query = "SELECT * FROM products WHERE name LIKE %s OR category LIKE %s"
    like_keyword = f"%{keyword}%"
    cursor.execute(query, (like_keyword, like_keyword))
    results = cursor.fetchall()
    for row in tree.get_children():
        tree.delete(row)
    for product in results:
        tree.insert("", END, values=product)

# Tkinter UI setup
root = Tk()
root.title("Inventory Management System")
root.geometry("700x500")

# Variables
name_var = StringVar()
category_var = StringVar()
quantity_var = StringVar()
price_var = StringVar()
search_var = StringVar()

# Widgets
Label(root, text="Product Name").place(x=20, y=20)
Entry(root, textvariable=name_var).place(x=120, y=20)

Label(root, text="Category").place(x=20, y=60)
Entry(root, textvariable=category_var).place(x=120, y=60)

Label(root, text="Quantity").place(x=20, y=100)
Entry(root, textvariable=quantity_var).place(x=120, y=100)

Label(root, text="Price").place(x=20, y=140)
Entry(root, textvariable=price_var).place(x=120, y=140)

Button(root, text="Add Product", command=add_product, width=15).place(x=20, y=180)
Button(root, text="Update Product", command=update_product, width=15).place(x=150, y=180)
Button(root, text="Delete Product", command=delete_product, width=15).place(x=280, y=180)

Label(root, text="Search").place(x=400, y=20)
Entry(root, textvariable=search_var).place(x=460, y=20)
Button(root, text="Search", command=search_products).place(x=600, y=16)

# Treeview for products
columns = ("ID", "Name", "Category", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    if col == "Name" or col == "Category":
        tree.column(col, width=150)
    else:
        tree.column(col, width=70)

tree.place(x=20, y=230, width=660, height=250)
tree.bind("<ButtonRelease-1>", select_product)

# Load products initially
load_products()

root.mainloop()
