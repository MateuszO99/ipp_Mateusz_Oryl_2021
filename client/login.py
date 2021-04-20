import tkinter as tk
from constans import LARGE_FONT, NORMAL_FONT
from check_length import check_length
from warnings_message import warning_message, clear
from repair_text import change_sign


class LoginPage(tk.Frame):
    """Create login frame"""
    def __init__(self, parent, controller):
        super(LoginPage, self).__init__(parent)

        self.controller = controller

        self.warning_msg = None

        title = tk.Label(self, text='Login', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        username = tk.Label(self, text='Username:', font=NORMAL_FONT)
        username.place(x=450, y=300, anchor='center')

        self.username_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.username_field.place(x=645, y=300, anchor='center')

        password = tk.Label(self, text='Password:', font=NORMAL_FONT)
        password.place(x=454, y=340, anchor='center')

        self.password_field = tk.Entry(self, show='*', width=20,
                                       font=NORMAL_FONT)
        self.password_field.place(x=645, y=340, anchor='center')

        login_button = tk.Button(self, text='Sign in', font=NORMAL_FONT,
                                 command=self.login)
        login_button.place(x=465, y=390, anchor='center')

        register_button = tk.Button(self, text='Create new account',
                                    font=NORMAL_FONT,
                                    command=self.go_to_register_page)
        register_button.place(x=630, y=390, anchor='center')

    def login(self):
        if len(self.username_field.get()) == 0 or \
                len(self.password_field.get()) == 0:
            warning_message(self, 'Your login or password\n are incorrect!',
                            [910, 320])
        else:
            username = change_sign(self.username_field)
            username = check_length(username, 255)

            password = change_sign(self.password_field)
            password = check_length(password, 255)

            message = f'login {username} {password}'
            receive_message = self.controller.connection.send_message(message)

            if receive_message == 'login_true_profile_true':
                self.clear_text()
                clear(self)
                self.controller.show_frame('MainPage')
            elif receive_message == 'login_true_profile_false':
                self.clear_text()
                self.controller.show_frame('ProfilePage')
            else:
                warning_message(
                    self,
                    'Your login or password\n are incorrect!',
                    [910, 320],
                )

    def go_to_register_page(self):
        clear(self)
        self.clear_text()
        self.controller.show_frame('RegisterPage')

    def clear_text(self):
        self.username_field.delete(0, 'end')
        self.password_field.delete(0, 'end')
