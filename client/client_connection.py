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
        message_length = f'{len(message):<{HEADER_SIZE}}'
        message = message_length + message
        self.client.send(message.encode(FORMAT))
        return self.receive_message()

    def receive_message(self):
        msg = ''
        msg_length = 0
        new_msg = True

        try:
            while True:
                message = self.client.recv(HEADER_SIZE)
                if new_msg:
                    msg_length = int(message)
                    new_msg = False
                    continue

                msg += message.decode(FORMAT)

                if msg_length == len(msg):
                    return msg

        except ValueError:
            return 'false'
