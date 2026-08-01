import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "database/shop.db"

class CategoryModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Category Management")
        self.root.geometry("700x500")

        tk.Label(
            self.root,
            text="Category Management",
            font=("Arial", 18, "bold")
        ).pack(pady=10)

        tk.Label(self.root, text="Category Name").pack()

        self.category_name = tk.Entry(self.root, width=40)
        self.category_name.pack(pady=5)

        tk.Button(
            self.root,
            text="Save Category",
            command=self.save_category
        ).pack(pady=10)

        self.tree = ttk.Treeview(
            self.root,
            columns=("ID", "Category"),
            show="headings"
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Category", text="Category")
        self.tree.pack(fill="both", expand=True)

        self.create_table()
        self.load_categories()

    def create_table(self):
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS categories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            )
        """)
        conn.commit()
        conn.close()

    def save_category(self):
        name = self.category_name.get().strip()
        if not name:
            messagebox.showwarning("Warning", "Enter category name")
            return

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO categories(name) VALUES(?)", (name,))
        conn.commit()
        conn.close()

        self.category_name.delete(0, tk.END)
        self.load_categories()

    def load_categories(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()
        conn.close()

        for row in rows:
            self.tree.insert("", "end", values=row)


if __name__ == "__main__":
    root = tk.Tk()
    CategoryModule(root)
    root.mainloop()
