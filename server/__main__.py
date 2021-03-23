from server_connection import ServerConnection


def main():
    connection = ServerConnection()
    connection.connection_establish()


if __name__ == '__main__':
    main()
