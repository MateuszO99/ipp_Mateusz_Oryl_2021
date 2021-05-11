import tkinter as tk
from datetime import datetime
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from constans import LARGE_FONT, NORMAL_FONT
from warnings_message import warning_message, clear
from check_length import check_length
from repair_text import change_sign


class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super(ProfilePage, self).__init__(parent)

        self.controller = controller

        self.file_name = None
        self.path = None
        self.profile_image = None

        self.warning_msg = None

        title = tk.Label(self, text='Profile information', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        name = tk.Label(self, text='Name:', font=NORMAL_FONT)
        name.place(x=475, y=300, anchor='center')

        self.name_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.name_field.place(x=645, y=300, anchor='center')

        last_name = tk.Label(self, text='Last name:', font=NORMAL_FONT)
        last_name.place(x=450, y=340, anchor='center')

        self.last_name_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.last_name_field.place(x=645, y=340, anchor='center')

        date = tk.Label(self, text='Date of birthday:', font=NORMAL_FONT)
        date.place(x=418, y=380, anchor='center')

        self.date_field = DateEntry(self, width=20, date_pattern='y-mm-dd',
                                    locale='en_US', font=NORMAL_FONT)
        self.date_field.place(x=654, y=367, anchor='n')

        profile_picture = tk.Label(self, text='Profile picture:',
                                   font=NORMAL_FONT)
        profile_picture.place(x=413, y=420, anchor='center')

        self.profile_picture_field = tk.Button(self, text='Select a picture',
                                               font=NORMAL_FONT,
                                               command=self.file_dialog)
        self.profile_picture_field.place(x=604, y=405, anchor='n')

        description = tk.Label(self, text='Describe yourself:',
                               font=NORMAL_FONT,)
        description.place(x=413, y=490, anchor='center')

        self.description_field = ScrolledText(self, width=30, height=7,
                                              font=NORMAL_FONT)
        self.description_field.place(x=718, y=480, anchor='n')

        accept_button = tk.Button(self, text='Accept', font=NORMAL_FONT,
                                  command=self.create_profile)
        accept_button.place(x=557, y=690, anchor='center')

    def file_dialog(self):
        self.file_name = askopenfilename(
            initialdir='/',
            title='Select a picture',
            filetype=(
                ('jpeg', '*.jpg'),
                ('png', '*.png'),
            ),
        )
        if self.path is not None:
            self.path.destroy()

        self.path = tk.Label(self, text='')
        self.path.configure(text=self.file_name)
        self.path.place(x=510, y=450, anchor='nw')

    def create_profile(self):
        if self.warning_msg is not None:
            self.warning_msg.destroy()

        if len(self.name_field.get()) == 0 or \
                len(self.last_name_field.get()) == 0 or \
                len(self.description_field.get('1.0', 'end-1c')) == 0 or \
                self.file_name is None or \
                len(self.file_name) == 0:
            warning_message(self, 'You have to enter data to all fields',
                            [950, 690])
        else:
            name = change_sign(self.name_field)
            name = check_length(name, 16)

            last_name = change_sign(self.last_name_field)
            last_name = check_length(last_name, 16)

            description = change_sign(self.description_field, True)
            description = check_length(description, 500)

            with open(self.file_name, 'rb') as image:
                self.profile_image = image.read()

            date_message = self.date_field.get()

            try:
                datetime.strptime(date_message, '%Y-%m-%d')
            except ValueError:
                warning_message(self, 'Wrong value in birthday field',
                                [950, 690])
            else:
                message = [name, last_name, date_message, description,
                           self.profile_image]

                receive_message = self.controller.connection
                receive = receive_message.send_message(message)

                if receive == 'profile_true':
                    self.clear_text()
                    clear(self)

                    if self.controller.cancel_button_status:
                        self.controller.show_frame('SettingsPage')
                    else:
                        self.controller.show_frame('MainPage')
                    self.controller.cancel_button_status = False
                else:
                    warning_message(self, 'You have to login first',
                                    [900, 690])

    def choose_button(self):
        if self.controller.cancel_button_status:
            self.cancel_button_draw()
        else:
            self.exit_button_draw()

    def cancel_button_draw(self):
        cancel_button = tk.Button(
            self,
            text='Cancel',
            font=NORMAL_FONT,
            width=6,
            command=self.cancel_button_command,
        )
        cancel_button.place(x=657, y=690, anchor='center')

    def cancel_button_command(self):
        self.controller.cancel_button_status = False
        self.controller.show_frame('SettingsPage')

    def exit_button_draw(self):
        cancel_button = tk.Button(
            self,
            text='Exit',
            font=NORMAL_FONT,
            width=6,
            command=lambda: tk.Tk.quit(self.controller),
        )
        cancel_button.place(x=657, y=690, anchor='center')

    def clear_text(self):
        self.name_field.delete(0, 'end')
        self.last_name_field.delete(0, 'end')
        self.description_field.delete(1.0, 'end')
        self.date_field.set_date(datetime.now())
        self.profile_image = None
        self.path.destroy()
