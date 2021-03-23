import queue
from client_connection import ClientConnection
from main_frame import MainFrame


def main():
    connection = ClientConnection()

    frame = MainFrame(connection)
    frame.mainloop()


if __name__ == '__main__':
    main()
