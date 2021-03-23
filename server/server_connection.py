import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER_SIZE = 10
FORMAT = "utf-8"


class ServerConnection:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))

        self.server.listen()

        self.client_socket = None
        self.address = None

    def connection_establish(self):
        """Establish connections with hosts"""
        while True:
            self.client_socket, self.address = self.server.accept()

            print(f'Connection from {self.address} has been establish')

            self.receive_code()

    def receive_code(self):
        msg = ''
        msg_length = 0
        new_msg = True

        try:
            while True:
                message = self.client_socket.recv(HEADER_SIZE)
                if new_msg:
                    msg_length = int(message)
                    new_msg = False
                    continue

                msg += message.decode(FORMAT)

                if msg_length == len(msg):
                    print(msg)
                    break
        except ValueError:
            pass
