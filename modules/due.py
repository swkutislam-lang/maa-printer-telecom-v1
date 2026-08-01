import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "database/shop.db"


class DueModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Due Management")
        self.root.geometry("900x500")

        title = tk.Label(
            self.root,
            text="Due Management",
            font=("Arial", 18, "bold"),
            bg="green",
            fg="white",
            pady=10,
        )
        title.pack(fill="x")

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Customer Name").grid(row=0, column=0, padx=5, pady=5)
        self.customer = tk.Entry(frame, width=25)
        self.customer.grid(row=0, column=1)

        tk.Label(frame, text="Mobile").grid(row=1, column=0, padx=5, pady=5)
        self.mobile = tk.Entry(frame, width=25)
        self.mobile.grid(row=1, column=1)

        tk.Label(frame, text="Due Amount").grid(row=2, column=0, padx=5, pady=5)
        self.amount = tk.Entry(frame, width=25)
        self.amount.grid(row=2, column=1)

        tk.Button(frame, text="Save", command=self.save_due, bg="green", fg="white").grid(row=3, column=0, pady=10)
        tk.Button(frame, text="Clear", command=self.clear).grid(row=3, column=1)

        self.table = ttk.Treeview(
            self.root,
            columns=("id", "customer", "mobile", "amount"),
            show="headings",
        )

        self.table.heading("id", text="ID")
        self.table.heading("customer", text="Customer")
        self.table.heading("mobile", text="Mobile")
        self.table.heading("amount", text="Due Amount")

        self.table.pack(fill="both", expand=True)

        self.create_table()
        self.load_data()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS due(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            mobile TEXT,
            amount REAL
        )
        """)

        conn.commit()
        conn.close()

    def save_due(self):
        customer = self.customer.get()
        mobile = self.mobile.get()
        amount = self.amount.get()

        if customer == "" or amount == "":
            messagebox.showerror("Error", "সব তথ্য পূরণ করুন")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO due(customer,mobile,amount) VALUES(?,?,?)",
            (customer, mobile, amount),
        )

        conn.commit()
        conn.close()

        self.load_data()
        self.clear()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        cur.execute("SELECT * FROM due")

        for row in cur.fetchall():
            self.table.insert("", "end", values=row)

        conn.close()

    def clear(self):
        self.customer.delete(0, tk.END)
        self.mobile.delete(0, tk.END)
        self.amount.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    DueModule(root)
    root.mainloop()
