import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "database/shop.db"

class Items:
    def __init__(self, root):
        self.root = root
        self.root.title("Items Management")
        self.root.geometry("800x600")

        tk.Label(root, text="Item Name").pack()
        self.item_name = tk.Entry(root, width=40)
        self.item_name.pack()

        tk.Label(root, text="Price").pack()
        self.price = tk.Entry(root, width=40)
        self.price.pack()

        tk.Button(root, text="Save Item", command=self.save_item).pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Name", "Price"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Price", text="Price")
        self.tree.pack(fill="both", expand=True)

        self.create_table()
        self.load_items()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                price REAL
            )
        """)
        conn.commit()
        conn.close()

    def save_item(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items(name, price) VALUES(?, ?)",
            (self.item_name.get(), self.price.get())
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Item Saved")
        self.load_items()

    def load_items(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        for row in cur.fetchall():
            self.tree.insert("", "end", values=row)
        conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    Items(root)
    root.mainloop()
