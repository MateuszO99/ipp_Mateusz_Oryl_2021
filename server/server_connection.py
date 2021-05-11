import socket
import pickle
import threading
import os
from data_management import DataManagement

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER_SIZE = 10
FORMAT = "utf-8"


class ServerConnection:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))

        self.server.listen()

        self.database_connection = DataManagement()

    def connection_establish(self):
        """Establish connections with hosts"""
        while True:
            client_socket, address = self.server.accept()

            thread = threading.Thread(target=self.receive_message,
                                      args=[client_socket, address],)
            thread.start()

    def receive_message(self, client_socket, address):
        print(f'Connection from {address} has been establish')

        user_id = None
        message_loop = True

        while message_loop:
            msg = b''
            msg_length = 0
            new_msg = True

            try:
                while True:
                    try:
                        message = client_socket.recv(HEADER_SIZE)
                    except ConnectionResetError:
                        break

                    if new_msg:
                        msg_length = int(message)
                        new_msg = False
                        continue

                    msg += message

                    if msg_length == len(msg):
                        msg = pickle.loads(msg)

                        if type(msg) == list:
                            self.profile(msg, client_socket, user_id)
                        else:
                            mode, *message_content = msg.split()
                            if mode == 'login':
                                user_id = self.login(message_content,
                                                     client_socket)
                            elif mode == 'register':
                                user_id = self.register(message_content,
                                                        client_socket)
                            elif mode == 'logout':
                                user_id = None
                                self.send_message('', client_socket)
                            elif mode == 'new_password':
                                self.change_password(message_content,
                                                     client_socket, user_id)
                            elif mode == 'delete':
                                self.delete_user(client_socket, user_id)
                            elif mode == 'user_profile':
                                self.display_user(user_id, client_socket)
                            elif mode == 'user_profiles':
                                self.display_users(user_id, client_socket,
                                                   message_content)
                        break

            except ValueError:
                pass

    def login(self, message, client_socket):
        username = message[0]
        password = ' '.join(message[1:])

        user_id = self.database_connection.check_user(username, password)

        if user_id:
            if self.database_connection.check_profile(user_id):
                self.send_message('login_true_profile_true', client_socket)
            else:
                self.send_message('login_true_profile_false', client_socket)
            return user_id
        else:
            self.send_message('login_false', client_socket)
            return None

    def register(self, message, client_socket):
        username = message[0]
        password = ' '.join(message[1:])

        user_id = self.database_connection.create_user(username, password)

        if user_id:
            self.send_message('register_true', client_socket)
            return user_id
        else:
            self.send_message('register_false', client_socket)
            return None

    def profile(self, message, client_socket, user_id):
        if user_id is not None:
            self.database_connection.profile_edition(
                message[0],
                message[1],
                message[2],
                message[3],
                message[4],
                user_id,
            )
            self.send_message('profile_true', client_socket)
        else:
            self.send_message('profile_false', client_socket)

    def change_password(self, message, client_socket, user_id):
        old_password = message[0]
        new_password = ' '.join(message[1:])

        msg = self.database_connection.change_password(user_id, old_password,
                                                       new_password)

        self.send_message(msg, client_socket)

    def delete_user(self, client_socket, user_id):
        image_name = self.database_connection.delete_user(user_id)
        try:
            os.remove(os.path.join('profile_images', image_name))
        except FileNotFoundError:
            pass

        self.send_message('deleted', client_socket)

    def display_user(self, user_id, client_socket):
        user_info = self.database_connection.user_info(user_id)
        user_info[5] = self.open_file(user_info[5])
        self.send_message(user_info, client_socket)

    def display_users(self, user_id, client_socket, current_value):
        current_value = int(current_value[0])
        user_info = self.database_connection.users_info(user_id, current_value)

        for i in range(5, 18, 6):
            try:
                user_info[i] = self.open_file(user_info[i])
            except IndexError:
                pass

        self.send_message(user_info, client_socket)

    @staticmethod
    def open_file(file_name):
        try:
            with open(os.path.join('profile_images', file_name), 'rb') \
                    as image:
                file_name = image.read()
        except FileNotFoundError:
            file_name = ''
        return file_name

    @staticmethod
    def send_message(message, client_socket):
        msg = pickle.dumps(message)
        msg = bytes(f'{len(msg):<{HEADER_SIZE}}', FORMAT) + msg

        client_socket.send(msg)
