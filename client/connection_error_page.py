import tkinter as tk
from constans import LARGE_FONT


class ConnectionErrorPage(tk.Frame):
    """Create register frame"""
    def __init__(self, parent, controller):
        super(ConnectionErrorPage, self).__init__(parent)

        self.controller = controller

        error_message = tk.Label(
            self,
            text='You can\'t connect with the server,\n'
                 'check your internet connection',
            font=LARGE_FONT,
            fg='red',
        )
        error_message.place(x=690, y=450, anchor='center')
