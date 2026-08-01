import tkinter as tk
from tkinter import ttk, messagebox
from database.db import get_connection


class Sales:
    def __init__(self, root):
        self.root = root
        self.root.title("Sales Management")
        self.root.geometry("1000x650")

        self.item_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.customer_var = tk.StringVar()

        title = tk.Label(
            self.root,
            text="Sales Management",
            bg="#0d6efd",
            fg="white",
            font=("Arial", 18, "bold")
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

        tk.Label(form, text="Quantity").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.qty_var).grid(row=1, column=1)

        tk.Label(form, text="Sale Price").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.price_var).grid(row=2, column=1)

        tk.Label(form, text="Customer").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(form, textvariable=self.customer_var).grid(row=3, column=1)

        tk.Button(
            form,
            text="Sell",
            bg="green",
            fg="white",
            command=self.sell_item
        ).grid(row=4, column=0, pady=10)

        tk.Button(
            form,
            text="Clear",
            command=self.clear
        ).grid(row=4, column=1, pady=10)

        self.table = ttk.Treeview(
            self.root,
            columns=("id", "item", "qty", "price", "customer"),
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("item", text="Item")
        self.table.heading("qty", text="Qty")
        self.table.heading("price", text="Price")
        self.table.heading("customer", text="Customer")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.create_table()
        self.load_items()
        self.load_sales()
          def create_table(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            CREATE TABLE IF NOT EXISTS sales(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                qty INTEGER,
                price REAL,
                customer TEXT,
                sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

    def sell_item(self):
        if self.item_var.get() == "":
            messagebox.showerror("Error", "Select Item")
            return

        if self.qty_var.get() == "":
            messagebox.showerror("Error", "Enter Quantity")
            return

        conn = get_connection()
        cur = conn.cursor()

        try:
            cur.execute("""
                INSERT INTO sales(item, qty, price, customer)
                VALUES(?,?,?,?)
            """, (
                self.item_var.get(),
                int(self.qty_var.get()),
                float(self.price_var.get()),
                self.customer_var.get()
            ))

            cur.execute("""
                UPDATE items
                SET qty = qty - ?
                WHERE name = ?
            """, (
                int(self.qty_var.get()),
                self.item_var.get()
            ))

            conn.commit()
            messagebox.showinfo("Success", "Sale Completed")

        except Exception as e:
            messagebox.showerror("Error", str(e))

        conn.close()

        self.load_sales()
        self.clear()
          def load_sales(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, item, qty, price, customer
            FROM sales
            ORDER BY id DESC
        """)

        rows = cur.fetchall()

        for row in rows:
            self.table.insert("", tk.END, values=row)

        conn.close()

    def clear(self):
        self.item_var.set("")
        self.qty_var.set("")
        self.price_var.set("")
        self.customer_var.set("")


if __name__ == "__main__":
    root = tk.Tk()
    Sales(root)
    root.mainloop()
