import tkinter as tk
from tkinter import ttk, messagebox

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("মা প্রিন্টার এন্ড টেলিকম Version 1.0")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f5f5f5")

        title = tk.Label(
            self.root,
            text="মা প্রিন্টার এন্ড টেলিকম",
            font=("Arial", 24, "bold"),
            bg="#0d6efd",
            fg="white",
            pady=15
        )
        title.pack(fill="x")

        menu = tk.Frame(self.root, bg="white")
        menu.pack(fill="x", pady=10)

        buttons = [
            "Category",
            "Items",
            "Stock",
            "Sales",
            "Due",
            "Reports",
            "Settings",
            "Backup",
            "Recycle Bin",
            "Logout"
        ]

        for text in buttons:
            tk.Button(
                menu,
                text=text,
                width=12,
                height=2
            ).pack(side="left", padx=5, pady=5)

        body = tk.Frame(self.root, bg="#f5f5f5")
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text="Dashboard",
            font=("Arial", 22, "bold"),
            bg="#f5f5f5"
        ).pack(pady=40)


if __name__ == "__main__":
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()
