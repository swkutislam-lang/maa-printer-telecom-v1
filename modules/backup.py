# Backup Module

import tkinter as tk

class BackupModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Backup")
        self.root.geometry("600x400")

        tk.Label(
            self.root,
            text="Backup Module (Coming Soon)",
            font=("Arial", 18, "bold")
        ).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    BackupModule(root)
    root.mainloop()
