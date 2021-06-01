import tkinter as tk
from constans import NORMAL_FONT


class MainPage(tk.Frame):
    """Create main page frame"""
    def __init__(self, parent, controller):
        super(MainPage, self).__init__(parent)

        self.controller = controller

        browse_button = tk.Button(
            self,
            text='Browse the profiles',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('BrowsProfilePage'),
            width=17,
        )
        browse_button.grid(row=0, column=0, padx=575, pady=(300, 10))

        messages_button = tk.Button(
            self,
            text='Messages',
            font=NORMAL_FONT,
            width=17,
            command=lambda: self.controller.show_frame('MessagesPage'),
        )
        messages_button.grid(row=1, column=0, pady=10)

        profile_button = tk.Button(
            self,
            text='My profile',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('DisplayProfilePage'),
            width=17,
        )
        profile_button.grid(row=2, column=0, pady=10)

        settings_button = tk.Button(
            self,
            text='Settings',
            font=NORMAL_FONT,
            command=lambda: self.controller.show_frame('SettingsPage'),
            width=17,
        )
        settings_button.grid(row=3, column=0, pady=10)

        logout_button = tk.Button(self, text='Log out', font=NORMAL_FONT,
                                  command=self.logout, width=17)
        logout_button.grid(row=4, column=0, pady=10)

        close_button = tk.Button(
            self,
            text='Close',
            font=NORMAL_FONT,
            command=lambda: tk.Tk.quit(self.controller),
            width=17,
        )
        close_button.grid(row=5, column=0, pady=10)

    def logout(self):
        self.controller.show_frame('LoginPage')
        message = f'logout'
        _ = self.controller.connection.send_message(message)
