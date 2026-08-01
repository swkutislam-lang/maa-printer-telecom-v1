import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection


class Stock:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Management")
        self.root.geometry("950x600")

        self.item_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.buy_price_var = tk.StringVar()
        self.supplier_var = tk.StringVar()

        title = tk.Label(
            self.root,
            text="Stock Management",
            font=("Arial", 18, "bold"),
            bg="#0d6efd",
            fg="white",
            pady=10
        )
        title.pack(fill="x")

        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Item").grid(row=0, column=0, padx=5, pady=5)
        self.item_combo = ttk.Combobox(
            form,
            textvariable=self.item_var,
            width=30,
            state="readonly"
        )
        self.item_combo.grid(row=0, column=1)

        tk.Label(form, text="Quantity").grid(row=1, column=0)
        tk.Entry(form, textvariable=self.qty_var).grid(row=1, column=1)

        tk.Label(form, text="Buy Price").grid(row=2, column=0)
        tk.Entry(form, textvariable=self.buy_price_var).grid(row=2, column=1)

        tk.Label(form, text="Supplier").grid(row=3, column=0)
        tk.Entry(form, textvariable=self.supplier_var).grid(row=3, column=1)

        tk.Button(
            form,
            text="Add Stock",
            command=self.add_stock,
            bg="green",
            fg="white"
        ).grid(row=4, column=0, pady=10)

        tk.Button(
            form,
            text="Clear",
            command=self.clear,
            bg="gray",
            fg="white"
        ).grid(row=4, column=1)

        self.table = ttk.Treeview(
            self.root,
            columns=("id", "item", "qty", "price", "supplier"),
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("item", text="Item")
        self.table.heading("qty", text="Quantity")
        self.table.heading("price", text="Buy Price")
        self.table.heading("supplier", text="Supplier")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_table()
        self.load_items()
        self.load_stock()
          def create_table(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS stock(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            qty INTEGER,
            buy_price REAL,
            supplier TEXT
        )
        """)

        conn.commit()
        conn.close()

    def load_items(self):
        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("SELECT name FROM items")
            rows = cur.fetchall()
            self.item_combo["values"] = [r[0] for r in rows]
        except:
            self.item_combo["values"] = []

        conn.close()

    def add_stock(self):
        if self.item_var.get() == "":
            messagebox.showerror("Error", "Select Item")
            return

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO stock(item, qty, buy_price, supplier)
        VALUES(?,?,?,?)
        """, (
            self.item_var.get(),
            self.qty_var.get(),
            self.buy_price_var.get(),
            self.supplier_var.get()
        ))

        try:
            cur.execute("""
            UPDATE items
            SET qty = qty + ?
            WHERE name=?
            """, (
                self.qty_var.get(),
                self.item_var.get()
            ))
        except:
            pass

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Stock Added Successfully")

        self.load_stock()
        self.clear()

    def load_stock(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT id,item,qty,buy_price,supplier
        FROM stock
        ORDER BY id DESC
        """)

        rows = cur.fetchall()

        for row in rows:
            self.table.insert("", tk.END, values=row)

        conn.close()

    def clear(self):
        self.item_var.set("")
        self.qty_var.set("")
        self.buy_price_var.set("")
        self.supplier_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    Stock(root)
    root.mainloop()
