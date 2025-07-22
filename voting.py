import mysql.connector
from tkinter import *
from tkinter import messagebox

# --------- Database Functions ---------
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # Your MySQL username
        password="hp22d6168",       # Your MySQL password
        database="votingdb"
    )

def add_candidate(name, party):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("INSERT INTO candidates (name, party) VALUES (%s, %s)", (name, party))
    conn.commit()
    conn.close()

def get_candidates():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM candidates")
    rows = cur.fetchall()
    conn.close()
    return rows

def cast_vote(voter_id, candidate_id):
    conn = connect_db()
    cur = conn.cursor()

    # Check if voter has already voted
    cur.execute("SELECT has_voted FROM voters WHERE voter_id=%s", (voter_id,))
    result = cur.fetchone()

    if result:
        if result[0]:
            conn.close()
            return False  # Already voted
        else:
            cur.execute("UPDATE voters SET has_voted=TRUE WHERE voter_id=%s", (voter_id,))
    else:
        cur.execute("INSERT INTO voters (voter_id, has_voted) VALUES (%s, TRUE)", (voter_id,))

    # Add vote
    cur.execute("UPDATE candidates SET votes = votes + 1 WHERE id=%s", (candidate_id,))
    conn.commit()
    conn.close()
    return True

def get_results():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT name, party, votes FROM candidates ORDER BY votes DESC")
    results = cur.fetchall()
    conn.close()
    return results

# --------- GUI ---------
def vote_screen():
    win = Toplevel()
    win.title("Cast Your Vote")

    Label(win, text="Enter Voter ID:").pack()
    voter_id_var = StringVar()
    Entry(win, textvariable=voter_id_var).pack(pady=5)

    Label(win, text="Choose a Candidate:").pack(pady=5)

    candidate_list = get_candidates()
    selected_candidate = IntVar()

    for c in candidate_list:
        Radiobutton(win, text=f"{c[1]} ({c[2]})", variable=selected_candidate, value=c[0]).pack(anchor="w")

    def submit_vote():
        voter_id = voter_id_var.get().strip()
        cid = selected_candidate.get()
        if voter_id and cid:
            success = cast_vote(voter_id, cid)
            if success:
                messagebox.showinfo("Success", "Vote cast successfully!")
            else:
                messagebox.showerror("Error", "You have already voted!")
        else:
            messagebox.showwarning("Missing Info", "Enter voter ID and select a candidate")

    Button(win, text="Submit Vote", command=submit_vote).pack(pady=10)

def admin_add_candidate():
    win = Toplevel()
    win.title("Add Candidate")

    Label(win, text="Name:").pack()
    name_var = StringVar()
    Entry(win, textvariable=name_var).pack()

    Label(win, text="Party:").pack()
    party_var = StringVar()
    Entry(win, textvariable=party_var).pack()

    def add():
        if name_var.get() and party_var.get():
            add_candidate(name_var.get(), party_var.get())
            messagebox.showinfo("Success", "Candidate added")
        else:
            messagebox.showwarning("Missing Info", "Please fill all fields")

    Button(win, text="Add Candidate", command=add).pack(pady=10)

def show_results():
    win = Toplevel()
    win.title("Voting Results")
    results = get_results()
    for res in results:
        Label(win, text=f"{res[0]} ({res[1]}) - {res[2]} votes").pack(anchor="w")

# --------- Main Window ---------
root = Tk()
root.title("Voting System")

Label(root, text="Voting System", font=("Arial", 16)).pack(pady=10)

Button(root, text="Vote", width=20, command=vote_screen).pack(pady=5)
Button(root, text="Admin: Add Candidate", width=20, command=admin_add_candidate).pack(pady=5)
Button(root, text="View Results", width=20, command=show_results).pack(pady=5)

root.mainloop()
