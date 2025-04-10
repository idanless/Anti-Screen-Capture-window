import tkinter as tk
import win32gui
import time
import threading


class Detection:
    def __init__(self):
        self.gui = tk.Tk()
        self.gui.overrideredirect(True)
        self.gui.attributes('-topmost', True)
        self.gui.geometry('350x100+100+10')  # Initial size and position
        self.gui.configure(bg='#2b2b2b')  # Dark background color
        self.gui.title("Focus Window Title")
        self.gui.resizable(False, False)

    def get_active_window_title(self):
        hwnd = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(hwnd)

    def initialize(self):
        # Frame to hold label and close button
        frame = tk.Frame(self.gui, bg='#2b2b2b', relief='solid', bd=1, padx=5, pady=5)
        frame.pack(fill='both', expand=True)

        # Close button ("X")
        close_btn = tk.Button(frame, text='✕', command=self.close_app,
                              fg='white', bg='#2b2b2b', bd=0, font=('Segoe UI', 12),
                              activebackground='#FF3B30', activeforeground='white',
                              relief='flat', highlightthickness=0)
        close_btn.pack(side='top', anchor='ne')

        # Label for window title with dynamic size and center alignment
        self.label = tk.Label(frame, text='', fg='lightgray', bg='#2b2b2b', font=('Helvetica', 10), anchor='center',
                              justify='center')
        self.label.pack(fill='both', expand=True, padx=10, pady=5)

        # Bind mouse for dragging
        self.label.bind('<Button-1>', self.start_move)
        self.label.bind('<B1-Motion>', self.do_move)
        frame.bind('<Button-1>', self.start_move)
        frame.bind('<B1-Motion>', self.do_move)

        # Subtle shadow effect
        self.gui.after(100, lambda: self.gui.config(bg='#333333'))

        threading.Thread(target=self.update_label, daemon=True).start()
        self.gui.mainloop()

    def update_label(self):
        while True:
            title = self.get_active_window_title()
            self.label.config(text=title if title else "No active window")

            # Get current position and adjust width based on title length
            current_geometry = self.gui.geometry().split('+')
            x_pos = current_geometry[1]
            y_pos = current_geometry[2]

            new_width = max(350, len(title) * 10)  # Adjust width based on title length
            self.gui.geometry(f'{new_width}x100+{x_pos}+{y_pos}')  # Keep current position

            time.sleep(0.5)

    def start_move(self, event):
        self.gui.x = event.x
        self.gui.y = event.y

    def do_move(self, event):
        x = self.gui.winfo_pointerx() - self.gui.x
        y = self.gui.winfo_pointery() - self.gui.y
        self.gui.geometry(f'+{x}+{y}')  # Update position as you drag

    def close_app(self, event=None):
        self.gui.destroy()


if __name__ == '__main__':
    GUI = Detection()
    GUI.initialize()
