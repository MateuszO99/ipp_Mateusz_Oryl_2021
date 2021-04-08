import socket
import threading
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

            threading.Thread(target=self.receive_message, args=[client_socket, address]).start()

    def receive_message(self, client_socket, address):
        print(f'Connection from {address} has been establish')

        user_id = None
        message_loop = True

        while message_loop:
            msg = ''
            msg_length = 0
            new_msg = True

            try:
                while True:
                    message = client_socket.recv(HEADER_SIZE)
                    if new_msg:
                        msg_length = int(message)
                        new_msg = False
                        continue

                    msg += message.decode(FORMAT)

                    if msg_length == len(msg):
                        user_id = self.authorisation(msg, client_socket)
                        break

            except ValueError:
                pass

    def authorisation(self, message, client_socket):
        mode, *msg = message.split()
        if mode == 'login':
            username = msg[0]
            password = ' '.join(msg[1:])

            user_id = self.database_connection.check_user(username, password)

            if user_id:
                self.send_message('login_true', client_socket)
                return user_id
            else:
                self.send_message('login_false', client_socket)
                return None
        elif mode == 'register':
            username = msg[0]
            password = ' '.join(msg[1:])

            user_id = self.database_connection.create_user(username, password)

            if user_id:
                self.send_message('register_true', client_socket)
                return user_id
            else:
                self.send_message('register_false', client_socket)
                return None

    @staticmethod
    def send_message(message, client_socket):
        message_length = f'{len(message):<{HEADER_SIZE}}'
        message = message_length + message

        client_socket.send(message.encode(FORMAT))
