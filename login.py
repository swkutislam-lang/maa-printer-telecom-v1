import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "database/shop.db"


def login():
    username = user_entry.get().strip()
    password = pass_entry.get().strip()

    if username == "" or password == "":
        messagebox.showerror("Error", "Username এবং Password দিন")
        return

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cur.execute("SELECT * FROM users")
    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO users(username,password) VALUES(?,?)",
            ("admin", "1234")
        )
        conn.commit()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    row = cur.fetchone()
    conn.close()

    if row:
        messagebox.showinfo("Success", "Login সফল")
        root.destroy()
        import dashboard
    else:
        messagebox.showerror("Error", "ভুল Username অথবা Password")


root = tk.Tk()
root.title("Maa Printer & Telecom - Login")
root.geometry("400x300")
root.resizable(False, False)

ttk.Label(root, text="Username").pack(pady=10)
user_entry = ttk.Entry(root, width=30)
user_entry.pack()

ttk.Label(root, text="Password").pack(pady=10)
pass_entry = ttk.Entry(root, width=30, show="*")
pass_entry.pack()

ttk.Button(root, text="Login", command=login).pack(pady=20)

root.mainloop()
