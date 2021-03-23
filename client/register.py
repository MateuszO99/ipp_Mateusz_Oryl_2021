import tkinter as tk
from constans import LARGE_FONT, NORMAL_FONT


class RegisterPage(tk.Frame):
    """Create register frame"""
    def __init__(self, parent, controller):
        super(RegisterPage, self).__init__(parent)

        title = tk.Label(self, text='Create new account', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        username = tk.Label(self, text='Username:', font=NORMAL_FONT)
        username.place(x=450, y=300, anchor='center')

        username_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        username_field.place(x=645, y=300, anchor='center')

        password1 = tk.Label(self, text='Password:', font=NORMAL_FONT)
        password1.place(x=454, y=340, anchor='center')

        password1_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        password1_field.place(x=645, y=340, anchor='center')

        password2 = tk.Label(self, text='Repeat password:', font=NORMAL_FONT)
        password2.place(x=413, y=380, anchor='center')

        password2_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        password2_field.place(x=645, y=380, anchor='center')

        login_button = tk.Button(self, text='Sign up', font=NORMAL_FONT)
        login_button.place(x=463, y=430, anchor='center')

        register_button = tk.Button(self, text='Login', font=NORMAL_FONT,
                                    command=lambda: controller.show_frame('LoginPage'))
        register_button.place(x=555, y=430, anchor='center')
