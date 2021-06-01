import tkinter as tk
from constans import NORMAL_FONT
from repair_text import change_sign


class SendMessagePage(tk.Frame):
    """Create login frame"""
    def __init__(self, parent, controller):
        super(SendMessagePage, self).__init__(parent)

        self.controller = controller
        self.parent = parent

        self.message = None
        self.display_messages = None

        tk.Label(self, text='Message:', font=NORMAL_FONT).\
            place(x=80, y=870, anchor='center')

        self.message = tk.Entry(self, width=80, font=NORMAL_FONT)
        self.message.place(x=660, y=870, anchor='center')

        send_button = tk.Button(self, text='Send', font=NORMAL_FONT,
                                command=self.send_msg)
        send_button.place(x=1240, y=870, anchor='center')

        back = tk.Button(self, text='Back', font=NORMAL_FONT,
                         command=self.back)
        back.place(x=1320, y=870, anchor='center')

    def send_msg(self):
        msg = change_sign(self.message)
        if len(msg) > 0 and not msg.isspace():
            message = f'message {self.controller.user_id} {msg}'
            _ = self.controller.connection.send_message(message)
            self.message.delete(0, 'end')

        self.update_msg()

    def back(self):
        self.controller.user_id = None
        self.controller.user_name = None
        self.message.delete(0, 'end')

        if self.controller.message_page:
            self.controller.show_frame('MessagesPage')
        else:
            self.controller.show_frame('BrowsProfilePage')

        self.display_messages.destroy()

    def update_msg(self):
        message = f'user_messages {self.controller.user_id}'
        messages = self.controller.connection.send_message(message)
        messages = [column for msg in messages for column in msg]

        formatted_messages = ''

        for ind, msg in enumerate(messages):
            if (ind + 2) % 4 == 0:
                msg = 'You' if msg == self.controller.user_id \
                    else self.controller.user_name
                formatted_messages += f'{msg}: '
            elif (ind + 1) % 4 == 0:
                formatted_messages += f'{msg}\n'

        self.display_messages = tk.Label(
            self,
            text=formatted_messages,
            font=NORMAL_FONT,
            wraplength=1350,
            justify='left',
        )
        self.display_messages.place(x=0, y=0, anchor='nw')
