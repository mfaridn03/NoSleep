import ctypes
import tkinter as tk
from tkinter import ttk


class Title:
    on = "NoSleep: ACTIVE"
    off = "NoSleep: OFF"


# https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate
ES_CONTINUOUS = 0x80000000
ES_DISPLAY_REQUIRED = 0x00000002


class NoSleepApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(Title.off)
        self.root.minsize(300, 200)

        window_width = 400
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")
        self.on = False

        self.lever_button = tk.Button(
            self.main_frame,
            text="OFF",
            command=self.toggle_state,
            font=("Arial", 16, "bold"),
            fg="red",
            width=10,
            height=2,
            relief=tk.RAISED,
            bd=3,
        )
        self.lever_button.pack(expand=True)

    def toggle_state(self):
        self.on = not self.on
        if self.on:
            self.lever_button.config(text="ON", fg="green")
            self.root.title(Title.on)
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_DISPLAY_REQUIRED
            )
        else:
            self.lever_button.config(text="OFF", fg="red")
            self.root.title(Title.off)
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = NoSleepApp()
    app.run()
