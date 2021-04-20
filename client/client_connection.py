import socket
import pickle
from constans import HEADER_SIZE

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
FORMAT = "utf-8"


class ClientConnection:
    def __init__(self):
        super(ClientConnection, self).__init__()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((IP, PORT))

    def send_message(self, message):
        """Send message to the server"""
        msg = pickle.dumps(message)
        msg = bytes(f'{len(msg):<{HEADER_SIZE}}', FORMAT) + msg
        self.client.send(msg)
        return self.receive_message()

    def receive_message(self):
        msg = b''
        msg_length = 0
        new_msg = True

        try:
            while True:
                message = self.client.recv(HEADER_SIZE)
                if new_msg:
                    msg_length = int(message)
                    new_msg = False
                    continue

                msg += message

                if msg_length == len(msg):
                    msg = pickle.loads(msg)
                    return msg

        except ValueError:
            return 'false'
