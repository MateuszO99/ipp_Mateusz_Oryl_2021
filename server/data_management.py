import os
import psycopg2

DB_NAME = 'tinder'
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = '127.0.0.1'
DB_PORT = '5432'


class DataManagement:
    def __init__(self):
        self.connection = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
        print('Database connected successfully')

    def check_user(self, username, password):
        with self.connection.cursor() as cur:
            cur.execute('SELECT * FROM user_account_table')

            rows = cur.fetchall()

            for row in rows:
                if username == row[1] and password == row[2]:
                    return row[0]

    def create_user(self, username, password):
        with self.connection.cursor() as cur:
            cur.execute(f"SELECT * FROM user_account_table WHERE username='{username}'")

            rows = cur.fetchall()

            if not rows:
                cur.execute(f"INSERT INTO user_account_table (username, password) VALUES ('{username}', '{password}')")

                cur.execute('SELECT * FROM user_account_table')

                rows = cur.fetchall()

                self.connection.commit()

                for row in rows:
                    if username == row[1]:
                        return row[0]
            else:
                self.connection.commit()

