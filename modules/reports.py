import tkinter as tk
from tkinter import ttk
import sqlite3

DB_NAME = "database/shop.db"


class ReportsModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Reports")
        self.root.geometry("900x600")

        title = tk.Label(
            self.root,
            text="Sales Report",
            bg="green",
            fg="white",
            font=("Arial", 18, "bold"),
            pady=10
        )
        title.pack(fill="x")

        summary = tk.Frame(self.root)
        summary.pack(fill="x", padx=10, pady=10)

        self.total_sales = tk.StringVar(value="0")
        self.total_profit = tk.StringVar(value="0")

        tk.Label(summary, text="Total Sales",
                 font=("Arial", 12, "bold")).grid(row=0, column=0, padx=20)

        tk.Label(summary,
                 textvariable=self.total_sales,
                 fg="blue",
                 font=("Arial", 14, "bold")).grid(row=1, column=0)

        tk.Label(summary, text="Total Profit",
                 font=("Arial", 12, "bold")).grid(row=0, column=1, padx=20)

        tk.Label(summary,
                 textvariable=self.total_profit,
                 fg="green",
                 font=("Arial", 14, "bold")).grid(row=1, column=1)

        self.table = ttk.Treeview(
            self.root,
            columns=("id", "item", "qty", "buy", "sell", "profit"),
            show="headings"
        )

        self.table.heading("id", text="ID")
        self.table.heading("item", text="Item")
        self.table.heading("qty", text="Qty")
        self.table.heading("buy", text="Buy Price")
        self.table.heading("sell", text="Sell Price")
        self.table.heading("profit", text="Profit")

        self.table.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_report()

    def load_report(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()

        try:
            cur.execute("""
                SELECT id,item_name,qty,buy_price,sell_price
                FROM sales
            """)
                      rows = cur.fetchall()

            total_sale = 0
            total_profit = 0

            for row in rows:
                sale = row[2] * row[4]
                profit = (row[4] - row[3]) * row[2]

                total_sale += sale
                total_profit += profit

                self.table.insert(
                    "",
                    "end",
                    values=(
                        row[0],
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        profit
                    )
                )

            self.total_sales.set(f"{total_sale:.2f}")
            self.total_profit.set(f"{total_profit:.2f}")

        except sqlite3.Error:
            pass

        conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    ReportsModule(root)
    root.mainloop()
