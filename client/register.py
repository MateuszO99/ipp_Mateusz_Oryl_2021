import tkinter as tk
from constans import LARGE_FONT, NORMAL_FONT
from warnings_message import warning_message, clear
from password_config import password_config, clear_text


class RegisterPage(tk.Frame):
    """Create register frame"""
    def __init__(self, parent, controller):
        super(RegisterPage, self).__init__(parent)

        self.controller = controller

        self.warning_msg = None

        title = tk.Label(self, text='Create new account', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        username = tk.Label(self, text='Username:', font=NORMAL_FONT)
        username.place(x=450, y=300, anchor='center')

        self.username_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.username_field.place(x=645, y=300, anchor='center')

        password1 = tk.Label(self, text='Password:', font=NORMAL_FONT)
        password1.place(x=454, y=340, anchor='center')

        self.password1_field = tk.Entry(self, show='*', width=20,
                                        font=NORMAL_FONT,)
        self.password1_field.place(x=645, y=340, anchor='center')

        password2 = tk.Label(self, text='Repeat password:', font=NORMAL_FONT)
        password2.place(x=413, y=380, anchor='center')

        self.password2_field = tk.Entry(self, show='*', width=20,
                                        font=NORMAL_FONT)
        self.password2_field.place(x=645, y=380, anchor='center')

        register_button = tk.Button(self, text='Sign up', font=NORMAL_FONT,
                                    command=self.register)
        register_button.place(x=463, y=430, anchor='center')

        login_button = tk.Button(self, text='Login', font=NORMAL_FONT,
                                 command=self.go_to_login_page)
        login_button.place(x=555, y=430, anchor='center')

    def register(self):
        coordinates = [960, 320]

        if len(self.username_field.get()) == 0 or \
                len(self.password1_field.get()) == 0 or \
                len(self.password2_field.get()) == 0:
            warning_message(self, 'You have to complete the form!',
                            coordinates)
        else:
            if not (' ' in self.username_field.get()):
                if self.password1_field.get() == self.password2_field.get():
                    if len(self.password1_field.get()) >= 8:
                        message = password_config(
                            self.username_field,
                            self.password1_field,
                            'register'
                        )

                        receive_message = self.controller.connection
                        msg = receive_message.send_message(message)

                        if msg == 'register_true':
                            clear(self)
                            clear_text(
                                self.username_field,
                                self.password1_field,
                                self.password2_field,
                            )
                            self.controller.show_frame('ProfilePage', True)
                        else:
                            warning_message(
                                self,
                                'This the username is unavailable!',
                                coordinates,
                            )

                    else:
                        warning_message(
                            self,
                            'Password is too short!\nAt least 8 character',
                            coordinates,
                        )
                else:
                    warning_message(self, 'Passwords are not the same!',
                                    coordinates)
            else:
                warning_message(self, 'Username have to be one word!',
                                coordinates)

    def go_to_login_page(self):
        clear(self)
        clear_text(
            self.username_field,
            self.password1_field,
            self.password2_field,
        )
        self.controller.show_frame('LoginPage')
