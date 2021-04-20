import datetime
import io
import tkinter as tk
from PIL import ImageTk, Image
from dateutil.relativedelta import relativedelta
from constans import NORMAL_FONT, SMALL_FONT


class DisplayProfilePage(tk.Frame):
    """Create main page frame"""
    def __init__(self, parent, controller):
        super(DisplayProfilePage, self).__init__(parent)

        self.controller = controller

        self.img = None
        self.user_name = None
        self.user_last_name = None
        self.user_birthday = None
        self.user_age = None
        self.user_description = None

        name = tk.Label(self, text='Name:', font=NORMAL_FONT)
        name.place(x=555, y=250, anchor='center')

        last_name = tk.Label(self, text='Last name:', font=NORMAL_FONT)
        last_name.place(x=530, y=300, anchor='center')

        birthday = tk.Label(self, text='Birthday:', font=NORMAL_FONT)
        birthday.place(x=540, y=350, anchor='center')

        age = tk.Label(self, text='Age:', font=NORMAL_FONT)
        age.place(x=760, y=350, anchor='center')

        description = tk.Label(self, text='Description:', font=NORMAL_FONT)
        description.place(x=524, y=400, anchor='center')

        back_button = tk.Button(
            self,
            text='Back',
            font=NORMAL_FONT,
            command=self.back,
        )
        back_button.place(x=524, y=470, anchor='center')

    def display(self):
        message = f'user_profile'
        receive_message = self.controller.connection.send_message(message)

        image_stream = io.BytesIO(receive_message[5])
        load = Image.open(image_stream)

        if load.height > 300 or load.width > 300:
            output_size = (300, 300)
            load.thumbnail(output_size)

        render = ImageTk.PhotoImage(load)
        self.img = tk.Label(self, image=render)
        self.img.image = render
        self.img.place(x=100, y=250)

        self.user_name = tk.Label(self, text=receive_message[1],
                                  font=NORMAL_FONT)
        self.user_name.place(x=590, y=250, anchor='w')

        self.user_last_name = tk.Label(self, text=receive_message[2],
                                       font=NORMAL_FONT)
        self.user_last_name.place(x=590, y=300, anchor='w')

        recv_date = receive_message[4]
        self.user_birthday = tk.Label(self, text=recv_date, font=NORMAL_FONT)
        self.user_birthday.place(x=590, y=350, anchor='w')

        now = datetime.datetime.now()
        date = datetime.datetime(recv_date.year, recv_date.month,
                                 recv_date.day)
        delta_time = relativedelta(now, date).years
        self.user_age = tk.Label(self, text=delta_time, font=NORMAL_FONT)
        self.user_age.place(x=785, y=350, anchor='w')

        self.user_description = tk.Label(self, text=receive_message[3],
                                         font=SMALL_FONT, wraplength=700,
                                         justify='left')
        self.user_description.place(x=590, y=393, anchor='nw')

    def back(self):
        self.img.destroy()
        self.user_name.destroy()
        self.user_last_name.destroy()
        self.user_birthday.destroy()
        self.user_age.destroy()
        self.user_description.destroy()

        self.controller.show_frame('MainPage')
