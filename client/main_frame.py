import tkinter as tk
from login import LoginPage
from register import RegisterPage


class MainFrame(tk.Tk):
    def __init__(self, connection, *args, **kwargs):
        """Create main frame of program"""
        super(MainFrame, self).__init__(*args, **kwargs)

        self.connection = connection

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, minsize=900, weight=1)
        container.grid_columnconfigure(0, minsize=1150, weight=1)

        self.frames = {}
        frame_list = (LoginPage, RegisterPage)

        for f in frame_list:
            frame = f(container, self)
            self.frames[f.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('LoginPage')

    def show_frame(self, controller):
        """Show frame which was passed as a parameter"""
        frame = self.frames[controller]
        frame.tkraise()
