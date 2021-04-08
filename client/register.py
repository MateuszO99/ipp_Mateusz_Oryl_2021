import tkinter as tk
from constans import LARGE_FONT, NORMAL_FONT
from check_length import check_length


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

        self.password1_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        self.password1_field.place(x=645, y=340, anchor='center')

        password2 = tk.Label(self, text='Repeat password:', font=NORMAL_FONT)
        password2.place(x=413, y=380, anchor='center')

        self.password2_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        self.password2_field.place(x=645, y=380, anchor='center')

        register_button = tk.Button(self, text='Sign up', font=NORMAL_FONT, command=self.register)
        register_button.place(x=463, y=430, anchor='center')

        login_button = tk.Button(self, text='Login', font=NORMAL_FONT,
                                 command=lambda: self.controller.show_frame('LoginPage'))
        login_button.place(x=555, y=430, anchor='center')

    def register(self):
        if len(self.username_field.get()) == 0 or len(self.password1_field.get()) == 0 \
                or len(self.password2_field.get()) == 0:
            self.warning_message('You have to complete the form!')
        else:
            if not (' ' in self.username_field.get()):
                if self.password1_field.get() == self.password2_field.get():
                    if len(self.password1_field.get()) >= 8:
                        username = check_length(self.username_field.get(), 255)
                        password = check_length(self.password1_field.get(), 255)

                        message = f'register {username} {password}'
                        receive_message = self.controller.connection.send_message(message)

                        if receive_message == 'register_true':
                            self.controller.show_frame('CreateProfilePage')
                        else:
                            self.warning_message('This the username is unavailable!')

                    else:
                        self.warning_message('Password is too short!\nAt least 8 character')
                else:
                    self.warning_message('Passwords are not the same!')
            else:
                self.warning_message('Username have to be one word!')

    def warning_message(self, text_message):
        if self.warning_msg is not None:
            self.warning_msg.destroy()

        self.warning_msg = tk.Label(self, text=text_message, font=NORMAL_FONT, fg='red')
        self.warning_msg.place(x=960, y=320, anchor='center')
