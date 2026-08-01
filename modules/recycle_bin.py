# Recycle Bin Module

import tkinter as tk

class RecycleBinModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Recycle Bin")
        self.root.geometry("600x400")

        tk.Label(
            self.root,
            text="Recycle Bin Module (Coming Soon)",
            font=("Arial", 18, "bold")
        ).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    RecycleBinModule(root)
    root.mainloop()
