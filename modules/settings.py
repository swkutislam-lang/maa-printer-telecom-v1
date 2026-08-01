# Settings Module

import tkinter as tk

class SettingsModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("600x400")

        tk.Label(
            self.root,
            text="Settings Module (Coming Soon)",
            font=("Arial", 18, "bold")
        ).pack(pady=50)

if __name__ == "__main__":
    root = tk.Tk()
    SettingsModule(root)
    root.mainloop()
