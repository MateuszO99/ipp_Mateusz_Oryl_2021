import tkinter as tk
from login import LoginPage
from register import RegisterPage
from profile_page import ProfilePage
from main_page import MainPage
from display_profile_page import DisplayProfilePage
from connection_error_page import ConnectionErrorPage
from browse_profile_page import BrowsProfilePage
from send_message import SendMessagePage
from messages import MessagesPage
from settings_page import (
    SettingsPage,
    ChangePasswordPage,
    DeleteAccountPage,
    CommunicatePage,
)


class MainFrame(tk.Tk):
    def __init__(self, connection, *args, **kwargs):
        """Create main frame of program"""
        super(MainFrame, self).__init__(*args, **kwargs)

        self.connection = connection
        self.cancel_button_status = False

        self.user_id = None
        self.user_name = None

        self.message_page = False

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, minsize=900, weight=1)
        container.grid_columnconfigure(0, minsize=1150, weight=1)

        self.frames = {}
        frame_list = (
            LoginPage, RegisterPage, ProfilePage, MainPage,
            SettingsPage, ConnectionErrorPage, ChangePasswordPage,
            DeleteAccountPage, CommunicatePage, DisplayProfilePage,
            BrowsProfilePage, SendMessagePage, MessagesPage
        )

        for f in frame_list:
            frame = f(container, self)
            self.frames[f.__name__] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        if self.connection is None:
            self.show_frame('ConnectionErrorPage')
        else:
            self.show_frame('LoginPage')

    def show_frame(self, controller, arg=False):
        """Show frame which was passed as a parameter"""
        frame = self.frames[controller]
        frame.tkraise()

        if arg:
            frame.choose_button()

        if controller == 'DisplayProfilePage' or \
                controller == 'BrowsProfilePage':
            frame.display()
        elif controller == 'SendMessagePage':
            frame.update_msg()
        elif controller == 'MessagesPage':
            frame.show_messages()
