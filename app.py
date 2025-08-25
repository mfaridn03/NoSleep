import tkinter as tk
from tkinter import ttk


class NoSleep:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("NoSleep")
        self.root.minsize(300, 200)

        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = NoSleep()
    app.run()
