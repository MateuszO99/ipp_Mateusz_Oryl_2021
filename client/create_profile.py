import tkinter as tk

from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkcalendar import DateEntry
from constans import LARGE_FONT, NORMAL_FONT


class CreateProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super(CreateProfilePage, self).__init__(parent)

        self.controller = controller

        self.file_name = None
        self.path = None

        title = tk.Label(self, text='Profile information', font=LARGE_FONT)
        title.place(x=555, y=250, anchor='center')

        name = tk.Label(self, text='Name:', font=NORMAL_FONT)
        name.place(x=475, y=300, anchor='center')

        self.name_field = tk.Entry(self, width=20, font=NORMAL_FONT)
        self.name_field.place(x=645, y=300, anchor='center')

        last_name = tk.Label(self, text='Last name:', font=NORMAL_FONT)
        last_name.place(x=450, y=340, anchor='center')

        self.last_name_field = tk.Entry(self, show='*', width=20, font=NORMAL_FONT)
        self.last_name_field.place(x=645, y=340, anchor='center')

        date = tk.Label(self, text='Date of birthday:', font=NORMAL_FONT)
        date.place(x=418, y=380, anchor='center')

        self.date_field = DateEntry(self, width=20, date_pattern='y-mm-dd', locale='en_US', font=NORMAL_FONT)
        self.date_field.place(x=654, y=367, anchor='n')

        profile_picture = tk.Label(self, text='Profile picture:', font=NORMAL_FONT)
        profile_picture.place(x=413, y=420, anchor='center')

        self.profile_picture_field = tk.Button(self, text='Select a picture', font=NORMAL_FONT,
                                               command=self.file_dialog)
        self.profile_picture_field.place(x=604, y=405, anchor='n')

        description = tk.Label(self, text='Describe yourself:', font=NORMAL_FONT)
        description.place(x=413, y=490, anchor='center')

        self.description_field = ScrolledText(self, width=30, height=7, font=NORMAL_FONT)
        self.description_field.place(x=718, y=480, anchor='n')

        accept_button = tk.Button(self, text='Accept', font=NORMAL_FONT)
        accept_button.place(x=557, y=690, anchor='center')

    def file_dialog(self):
        self.file_name = askopenfilename(initialdir='/', title='Select a picture',
                                         filetype=(('jpeg', '*.jpg'), ('png', '*.png'), ('All Files', '*.*')))
        if self.path is not None:
            self.path.destroy()

        self.path = tk.Label(self, text='')
        self.path.configure(text=self.file_name)
        self.path.place(x=510, y=450, anchor='nw')
