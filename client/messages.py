import tkinter as tk
from constans import NORMAL_FONT


class MessagesPage(tk.Frame):
    """Create login frame"""
    def __init__(self, parent, controller):
        super(MessagesPage, self).__init__(parent)

        self.controller = controller

        self.all_labels = []
        self.message_button = []

        back_button = tk.Button(
            self,
            text='Back',
            font=NORMAL_FONT,
            command=self.back,
        )
        back_button.place(x=1300, y=850, anchor='center')

    def show_messages(self):
        self.controller.message_page = True

        message = f'all_messages'
        receive_message = self.controller.connection.send_message(message)

        message = f'all_messages_names'
        names = self.controller.connection.send_message(message)

        message = f'my_id'
        user_id = self.controller.connection.send_message(message)

        all_messages = []

        for msg in receive_message:
            x = True
            for i in range(len(all_messages)):
                if (all_messages[i][1] == msg[1]
                    and all_messages[i][2] == msg[2]) \
                        or (all_messages[i][1] == msg[2]
                            and all_messages[i][2] == msg[1]):
                    all_messages[i] = msg
                    x = False
                    break

            if x:
                all_messages.append(msg)

        y = 50

        for msg_index, msg in enumerate(all_messages):
            user_name = None
            target_id = None
            if user_id == msg[1]:
                target_id = msg[2]
                for name in names:
                    if name[0] == msg[2]:
                        user_name = name[1]
                        break
            else:
                target_id = msg[1]
                for name in names:
                    if name[0] == msg[1]:
                        user_name = name[1]
                        break

            content = msg[3]
            if len(content) > 75:
                content = f'{content[:75]}...'

            self.all_labels.append(tk.Label(
                self,
                text=f'{user_name}\n{content}',
                font=NORMAL_FONT,
                justify=tk.LEFT,
            ))
            self.all_labels[msg_index].place(x=50, y=y, anchor='w')

            self.message_button.append(tk.Button(
                self,
                text='Send message',
                font=NORMAL_FONT,
                command=lambda t_id=target_id, u_name=user_name:
                self.send_message(
                    t_id,
                    u_name,
                )
            ))
            self.message_button[msg_index].place(x=50, y=y+50, anchor='w')

            y += 150

    def send_message(self, user_id, user_name):
        self.controller.user_id = user_id
        self.controller.user_name = user_name
        self.clear()
        self.controller.show_frame('SendMessagePage')

    def back(self):
        self.clear()
        self.controller.message_page = False
        self.controller.show_frame('MainPage')

    def clear(self):
        for i in range(len(self.all_labels)):
            try:
                self.all_labels[i].destroy()
                self.message_button[i].destroy()
            except IndexError:
                pass

        self.all_labels = []
        self.message_button = []
