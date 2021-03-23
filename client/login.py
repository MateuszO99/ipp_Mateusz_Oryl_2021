import tkinter as tk
from constans import LARGE_FONT, NORMAL_FONT


class LoginPage(tk.Frame):
    """Create login frame"""
    def __init__(self, parent, controller):
        super(LoginPage, self).__init__(parent)

        self.controller = controller

        title = tk.Label(self, text='Login', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        username = tk.Label(self, text='Username:', font=NORMAL_FONT)
        username.place(x=450, y=300, anchor='center')

        self.username_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.username_field.place(x=645, y=300, anchor='center')

        password = tk.Label(self, text='Password:', font=NORMAL_FONT)
        password.place(x=454, y=340, anchor='center')

        self.password_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        self.password_field.place(x=645, y=340, anchor='center')

        login_button = tk.Button(self, text='Sign in', font=NORMAL_FONT,
                                 command=lambda: self.login())
        login_button.place(x=465, y=390, anchor='center')

        register_button = tk.Button(self, text='Create new account', font=NORMAL_FONT,
                                    command=lambda: self.controller.show_frame('RegisterPage'))
        register_button.place(x=630, y=390, anchor='center')

    def login(self):
        if len(self.username_field.get()) == 0 or len(self.password_field.get()) == 0:
            warning_message = tk.Label(self, text='Your login or password\n are incorrect!', font=NORMAL_FONT, fg='red')
            warning_message.place(x=910, y=320, anchor='center')
        else:
            message = f'{self.username_field.get()} {self.password_field.get()}'
            self.controller.connection.send_message(message)
