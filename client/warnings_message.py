import tkinter as tk

from constans import NORMAL_FONT


def clear(self):
    if self.warning_msg is not None:
        self.warning_msg.destroy()


def warning_message(self, text_message, coordinates, color='red'):
    clear(self)

    self.warning_msg = tk.Label(self, text=text_message, font=NORMAL_FONT,
                                fg=color)
    self.warning_msg.place(x=coordinates[0], y=coordinates[1], anchor='center')
