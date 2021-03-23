import socket

IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
HEADER_SIZE = 10
FORMAT = "utf-8"


class ClientConnection:
    def __init__(self):
        super(ClientConnection, self).__init__()

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((IP, PORT))

    def send_message(self, message):
        """Send message to the server"""
        message = f'login {message}'
        message_length = f'{len(message):<{HEADER_SIZE}}'
        message = message_length + message

        self.client.send(message.encode(FORMAT))
