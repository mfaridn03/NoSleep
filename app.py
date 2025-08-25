import ctypes
import tkinter as tk
from tkinter import ttk
import random


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
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

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

        self.BTN_OFF_COLOUR = "#ffd7d7"
        self.BTN_ON_COLOUR = "#d7ffd7"

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
            bg=self.BTN_OFF_COLOUR,
        )
        # Use absolute positioning for animation (DVD-style bounce)
        self.lever_button.place(x=0, y=0)

        # Animation state
        self.frame_interval_ms = 16  # ~60 FPS
        self.animation_running = True
        self.animation_id = None
        self.pos_x = 0
        self.pos_y = 0
        # Randomize initial velocity (ensure non-zero components)
        self.vel_x = random.choice([-1, 1]) * random.randint(3, 6)
        self.vel_y = random.choice([-1, 1]) * random.randint(2, 5)

        # Defer animation start until sizes are realized
        self.root.after(50, self.start_animation)

    def toggle_state(self):
        self.on = not self.on
        if self.on:
            self.lever_button.config(text="ON", fg="green", bg=self.BTN_ON_COLOUR)
            self.root.title(Title.on)
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_DISPLAY_REQUIRED
            )
        else:
            self.lever_button.config(text="OFF", fg="red", bg=self.BTN_OFF_COLOUR)
            self.root.title(Title.off)
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)

    def start_animation(self):
        # Ensure geometry is computed
        self.root.update_idletasks()

        frame_w = self.main_frame.winfo_width()
        frame_h = self.main_frame.winfo_height()
        btn_w = self.lever_button.winfo_width()
        btn_h = self.lever_button.winfo_height()

        # If sizes aren't ready yet, try again shortly
        if frame_w <= 1 or frame_h <= 1 or btn_w <= 1 or btn_h <= 1:
            self.root.after(50, self.start_animation)
            return

        # Randomize initial position within bounds
        max_x = max(0, frame_w - btn_w)
        max_y = max(0, frame_h - btn_h)
        self.pos_x = random.randint(0, max_x)
        self.pos_y = random.randint(0, max_y)
        self.lever_button.place(x=self.pos_x, y=self.pos_y)

        # Start the animation loop
        self.animate()

    def animate(self):
        if not self.animation_running:
            return

        frame_w = self.main_frame.winfo_width()
        frame_h = self.main_frame.winfo_height()
        btn_w = self.lever_button.winfo_width()
        btn_h = self.lever_button.winfo_height()

        # Update position
        next_x = self.pos_x + self.vel_x
        next_y = self.pos_y + self.vel_y

        # Horizontal bounce
        if next_x <= 0:
            next_x = 0
            self.vel_x = abs(self.vel_x)
        elif next_x + btn_w >= frame_w:
            next_x = max(0, frame_w - btn_w)
            self.vel_x = -abs(self.vel_x)

        # Vertical bounce
        if next_y <= 0:
            next_y = 0
            self.vel_y = abs(self.vel_y)
        elif next_y + btn_h >= frame_h:
            next_y = max(0, frame_h - btn_h)
            self.vel_y = -abs(self.vel_y)

        self.pos_x = next_x
        self.pos_y = next_y
        self.lever_button.place(x=int(self.pos_x), y=int(self.pos_y))

        # Queue next frame
        self.animation_id = self.root.after(self.frame_interval_ms, self.animate)

    def run(self):
        self.root.mainloop()

    def on_close(self):
        # Stop animation loop safely
        self.animation_running = False
        if self.animation_id is not None:
            try:
                self.root.after_cancel(self.animation_id)
            except Exception:
                pass
        if self.on:
            ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        self.root.destroy()


if __name__ == "__main__":
    app = NoSleepApp()
    app.run()
