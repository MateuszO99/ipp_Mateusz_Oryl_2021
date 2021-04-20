import tkinter as tk
from constans import NORMAL_FONT, LARGE_FONT
from warnings_message import warning_message, clear
from password_config import password_config, clear_text


class SettingsPage(tk.Frame):
    """Create Settings frame"""

    def __init__(self, parent, controller):
        super(SettingsPage, self).__init__(parent)

        self.controller = controller

        profile_button = tk.Button(
            self,
            text='Edit Profile',
            font=NORMAL_FONT,
            width=17,
            command=self.go_to_profile_page,
        )
        profile_button.grid(row=0, column=0, padx=575, pady=(300, 10))

        password_button = tk.Button(
            self,
            text='Change Password',
            font=NORMAL_FONT,
            width=17,
            command=lambda: self.controller.show_frame('ChangePasswordPage'),
        )
        password_button.grid(row=1, column=0, pady=10)

        delete_button = tk.Button(
            self,
            text='Delete Account',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('DeleteAccountPage'),
            width=17,
        )
        delete_button.grid(row=2, column=0, pady=10)

        back_button = tk.Button(
            self,
            text='Back',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('MainPage'),
            width=17,
        )
        back_button.grid(row=3, column=0, pady=10)

    def go_to_profile_page(self):
        self.controller.cancel_button_status = True
        self.controller.show_frame('ProfilePage', True)


class ChangePasswordPage(tk.Frame):
    def __init__(self, parent, controller):
        super(ChangePasswordPage, self).__init__(parent)

        self.controller = controller

        self.warning_msg = None

        old_password = tk.Label(self, text='Old password:', font=NORMAL_FONT)
        old_password.place(x=504, y=300, anchor='center')

        self.old_password_field = tk.Entry(self, show='*', width=20,
                                           font=NORMAL_FONT,)
        self.old_password_field.place(x=730, y=300, anchor='center')

        new_password1 = tk.Label(self, text='New password:', font=NORMAL_FONT)
        new_password1.place(x=500, y=340, anchor='center')

        self.new_password1_field = tk.Entry(self, show='*', width=20,
                                            font=NORMAL_FONT)
        self.new_password1_field.place(x=730, y=340, anchor='center')

        new_password2 = tk.Label(self, text='Repeat new password:',
                                 font=NORMAL_FONT)
        new_password2.place(x=463, y=380, anchor='center')

        self.new_password2_field = tk.Entry(self, show='*', width=20,
                                            font=NORMAL_FONT)
        self.new_password2_field.place(x=730, y=380, anchor='center')

        change_password_button = tk.Button(self, text='Change password',
                                           font=NORMAL_FONT,
                                           command=self.change_password)
        change_password_button.place(x=480, y=430, anchor='center')

        back_button = tk.Button(self, text='Back', font=NORMAL_FONT,
                                command=self.back_function, width=17)
        back_button.place(x=710, y=430, anchor='center')

    def change_password(self):
        coordinates = [1060, 320]

        if len(self.old_password_field.get()) == 0 or \
                len(self.new_password1_field.get()) == 0 or \
                len(self.new_password2_field.get()) == 0:
            warning_message(self, 'You have to complete the form!',
                            coordinates)
        elif not self.new_password1_field.get() == \
                self.new_password2_field.get():
            warning_message(self, 'Passwords are not the same!', coordinates)
        else:
            if len(self.new_password1_field.get()) >= 8:
                message = password_config(
                    self.old_password_field,
                    self.new_password1_field,
                    'new_password'
                )

                receive_message = self.controller.connection
                msg = receive_message.send_message(message)

                if msg == 'new_password_true':
                    clear_text(
                        self.old_password_field,
                        self.new_password1_field,
                        self.new_password2_field,
                    )
                    warning_message(self, 'Password has been changed',
                                    coordinates, 'green')
                else:
                    warning_message(self, 'Wrong password', coordinates)
            else:
                warning_message(self, 'New password is too short', coordinates)

    def back_function(self):
        clear(self)
        clear_text(
            self.old_password_field,
            self.new_password1_field,
            self.new_password2_field,
        )
        self.controller.show_frame('SettingsPage')


class DeleteAccountPage(tk.Frame):
    def __init__(self, parent, controller):
        super(DeleteAccountPage, self).__init__(parent)

        self.controller = controller

        warning = tk.Label(
            self,
            text='Are you sure you want to delete this account?',
            font=LARGE_FONT,
            fg='red',
        )
        warning.place(x=690, y=300, anchor='center')

        yes_button = tk.Button(
            self,
            text='Yes',
            font=NORMAL_FONT,
            command=self.delete_account,
            width=17,
        )
        yes_button.place(x=560, y=430, anchor='center')

        no_button = tk.Button(
            self,
            text='No',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('SettingsPage'),
            width=17,
        )
        no_button.place(x=820, y=430, anchor='center')

    def delete_account(self):
        message = f'delete'
        self.controller.connection.send_message(message)

        self.controller.show_frame('CommunicatePage')


class CommunicatePage(tk.Frame):
    def __init__(self, parent, controller):
        super(CommunicatePage, self).__init__(parent)

        self.controller = controller

        info = tk.Label(
            self,
            text='Your account has been deleted',
            font=LARGE_FONT,
            fg='red',
        )
        info.place(x=690, y=300, anchor='center')

        login_button = tk.Button(
            self,
            text='Sign in',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('LoginPage'),
            width=17,
        )
        login_button.place(x=560, y=430, anchor='center')

        register_button = tk.Button(
            self,
            text='Sign up',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('RegisterPage'),
            width=17,
        )
        register_button.place(x=820, y=430, anchor='center')
