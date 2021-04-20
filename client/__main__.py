from client_connection import ClientConnection
from main_frame import MainFrame


def main():
    try:
        connection = ClientConnection()
    except ConnectionRefusedError:
        connection = None

    frame = MainFrame(connection)
    frame.mainloop()


if __name__ == '__main__':
    main()
