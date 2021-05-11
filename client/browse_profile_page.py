import datetime
import io
import tkinter as tk
from PIL import ImageTk, Image
from dateutil.relativedelta import relativedelta
from constans import SMALL_FONT, NORMAL_FONT


class BrowsProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super(BrowsProfilePage, self).__init__(parent)

        self.controller = controller

        self.current_value = 0

        self.img = []
        self.user_full_name = []
        self.user_age = []
        self.user_description = []

        self.previous_button = None
        self.next_button = None

        back_button = tk.Button(
            self,
            text='Back',
            font=NORMAL_FONT,
            command=self.back,
        )
        back_button.place(x=1300, y=850, anchor='center')

    def display(self):
        if self.current_value:
            self.previous_button = tk.Button(
                self,
                text='Previous',
                font=NORMAL_FONT,
                command=self.previous,
            )
            self.previous_button.place(x=75, y=150, anchor='center')

        message = f'user_profiles {self.current_value}'
        receive_message = self.controller.connection.send_message(message)
        j = 0

        if receive_message[-1] > self.current_value + 3:
            self.next_button = tk.Button(
                self,
                text='Next',
                font=NORMAL_FONT,
                command=self.next,
            )
            self.next_button.place(x=1300, y=150, anchor='center')

        for i in range(0, 13, 6):
            try:
                x = 150 + j*375
                image_stream = io.BytesIO(receive_message[i+5])
                load = Image.open(image_stream)

                if load.height > 300 or load.width > 300:
                    output_size = (300, 300)
                    load.thumbnail(output_size)

                render = ImageTk.PhotoImage(load)
                self.img.append(tk.Label(self, image=render))
                self.img[j].image = render
                self.img[j].place(x=x, y=50)

                self.user_full_name.append(tk.Label(
                    self,
                    text=f'{receive_message[i+1]} {receive_message[i+2]}',
                    font=SMALL_FONT,
                ))
                self.user_full_name[j].place(x=x, y=375, anchor='w')

                recv_date = receive_message[i+4]

                now = datetime.datetime.now()
                date = datetime.datetime(recv_date.year, recv_date.month,
                                         recv_date.day)
                delta_time = relativedelta(now, date).years
                self.user_age.append(tk.Label(self, text=f'Age: {delta_time}',
                                     font=SMALL_FONT))
                self.user_age[j].place(x=x, y=400, anchor='w')

                self.user_description.append(tk.Label(
                    self,
                    text=receive_message[i+3],
                    font=SMALL_FONT, wraplength=300,
                    justify='left',
                ))
                self.user_description[j].place(x=x, y=420, anchor='nw')

                j += 1
            except IndexError:
                pass

    def back(self):
        self.clear()

        self.current_value = 0

        self.controller.show_frame('MainPage')

    def next(self):
        self.clear()
        self.current_value += 3
        self.controller.show_frame('BrowsProfilePage')

    def previous(self):
        self.clear()
        self.current_value -= 3
        self.controller.show_frame('BrowsProfilePage')

    def clear(self):
        for i in range(3):
            try:
                self.img[i].destroy()
                self.user_full_name[i].destroy()
                self.user_age[i].destroy()
                self.user_description[i].destroy()
            except IndexError:
                pass

        self.img = []
        self.user_full_name = []
        self.user_age = []
        self.user_description = []

        if self.previous_button:
            self.previous_button.destroy()

        if self.next_button:
            self.next_button.destroy()
