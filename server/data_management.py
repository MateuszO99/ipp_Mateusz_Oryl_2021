import os
import re
import string
import random
import psycopg2

DB_NAME = 'tinder'
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = '127.0.0.1'
DB_PORT = '5432'


def create_file_name():
    while True:
        file_name = ''
        for _ in range(15):
            file_name += random.choice(string.ascii_letters)
        file_name += '.jpg'

        path = os.path.join('profile_images', file_name)
        if not os.path.exists(path):
            break
    return path


def change_sign(text):
    regex = re.compile("'")
    return regex.sub("''", text)


def create_file(image):
    file_name = create_file_name()
    with open(file_name, 'wb') as file:
        file.write(image)
    return os.path.basename(file_name)


class DataManagement:
    def __init__(self):
        try:
            self.connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
            )
            print('Database connected successfully')

        except psycopg2.OperationalError:
            self.create_database()

            self.connection = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASS,
                host=DB_HOST,
                port=DB_PORT,
            )

            self.create_tables()

    @staticmethod
    def create_database():
        connection = psycopg2.connect(
            database='postgres',
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
        )

        connection.autocommit = True

        with connection.cursor() as cur:
            cur.execute(f"CREATE database {DB_NAME};")

        print("Database created successfully")

    def create_tables(self):
        with self.connection.cursor() as cur:
            cur.execute("CREATE TABLE user_account_table ("
                        "user_id INT NOT NULL PRIMARY KEY "
                        "GENERATED ALWAYS AS IDENTITY,"
                        "username VARCHAR(255) NOT NULL,"
                        "password VARCHAR(255) NOT NULL);")

            cur.execute("CREATE TABLE user_table ("
                        "user_id INT,"
                        "name VARCHAR(255) NOT NULL,"
                        "last_name VARCHAR(255) NOT NULL,"
                        "description VARCHAR(2000) NOT NULL,"
                        "birthday date,"
                        "profile_image TEXT NOT NULL);")

            cur.execute("CREATE TABLE messages ("
                        "message_id INT NOT NULL PRIMARY KEY "
                        "GENERATED ALWAYS AS IDENTITY, "
                        "user_id1 INT, "
                        "user_id2 INT, "
                        "content TEXT)")
        self.connection.commit()
        print('Tables created successfully')

    def check_user(self, username, password):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM user_account_table")

            rows = cur.fetchall()

            for row in rows:
                if username == change_sign(row[1]) and \
                        password == change_sign(row[2]):
                    return row[0]

    def create_user(self, username, password):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM user_account_table "
                        f"WHERE username='{username}'")

            rows = cur.fetchall()

            if not rows:
                cur.execute("INSERT INTO user_account_table "
                            "(username, password) "
                            f"VALUES ('{username}', '{password}')")

                self.connection.commit()

                cur.execute("SELECT * FROM user_account_table")

                rows = cur.fetchall()

                for row in rows:
                    if username == change_sign(row[1]):
                        return row[0]

    def profile_edition(self, name, last_name, birthday, description, image,
                        user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM user_table "
                        f"WHERE user_id='{user_id}'")

            rows = cur.fetchall()

            if rows:

                cur.execute("SELECT profile_image FROM user_table "
                            f"WHERE user_id = {user_id}")

                image_name = cur.fetchall()

                try:
                    os.remove(os.path.join('profile_images', image_name[0][0]))
                except FileNotFoundError:
                    pass

                file_name = create_file(image)
                cur.execute("UPDATE user_table SET "
                            f"user_id={user_id}, name='{name}', "
                            f"last_name='{last_name}', "
                            f"description='{description}', "
                            f"birthday='{birthday}', "
                            f"profile_image='{file_name}'"
                            f"WHERE user_id = {user_id};")

            else:
                file_name = create_file(image)
                cur.execute("INSERT INTO user_table( "
                            "user_id, name, last_name, description, birthday, "
                            "profile_image) VALUES ("
                            f"{user_id}, '{name}', '{last_name}', "
                            f"'{description}', '{birthday}', '{file_name}')")

            self.connection.commit()

    def check_profile(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT user_id FROM user_table "
                        f"WHERE user_id = {user_id}")

            rows = cur.fetchall()
            return len(rows)

    def change_password(self, user_id, old_password, new_password):
        with self.connection.cursor() as cur:
            cur.execute("SELECT user_id FROM user_account_table "
                        f"WHERE user_id = {user_id} "
                        f"AND password='{old_password}'")

            rows = cur.fetchall()

            if len(rows) == 1:
                cur.execute("UPDATE user_account_table "
                            f"SET password = '{new_password}' "
                            f"WHERE user_id = {rows[0][0]};")
                self.connection.commit()

                return 'new_password_true'
            return 'False'

    def delete_user(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT profile_image FROM user_table "
                        f"WHERE user_id = {user_id}")

            image_name = cur.fetchall()

            cur.execute("DELETE FROM user_table "
                        f"WHERE user_id = {user_id}")

            cur.execute("DELETE FROM user_account_table "
                        f"WHERE user_id = {user_id}")

            self.connection.commit()

            return image_name[0][0]

    def user_info(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM user_table "
                        f"WHERE user_id = {user_id}")

            columns = cur.fetchall()

            information = [column for column in columns[0]]

            return information

    def users_info(self, user_id, current_value):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM user_table "
                        f"WHERE user_id <> {user_id} "
                        "ORDER BY user_id DESC "
                        f"OFFSET {current_value} "
                        "FETCH FIRST 3 ROWS ONLY;")

            rows = cur.fetchall()

            information = []

            for row in rows:
                for column in row:
                    information.append(column)

            cur.execute("SELECT * FROM user_table "
                        f"WHERE user_id <> {user_id};")
            user_number = len(cur.fetchall())

            information.append(user_number)

            return information

    def create_msg(self, user_id, target_user_id, message):
        with self.connection.cursor() as cur:
            cur.execute("INSERT INTO messages "
                        "(user_id1, user_id2, content) "
                        f"VALUES ('{user_id}', '{target_user_id}', "
                        f"'{message}')")

            self.connection.commit()

    def display_messages(self, user_id, target_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM messages "
                        f"WHERE (user_id1 = {user_id} "
                        f"AND user_id2 = {target_id}) "
                        f"OR (user_id1 = {target_id} "
                        f"AND user_id2 = {user_id})")

            columns = cur.fetchall()

            return columns

    def display_all_messages(self, user_id):
        with self.connection.cursor() as cur:
            cur.execute("SELECT * FROM messages "
                        f"WHERE user_id1 = {user_id} "
                        f"OR user_id2 = {user_id}")

            columns = cur.fetchall()

            return columns

    def display_all_names(self):
        with self.connection.cursor() as cur:
            cur.execute("SELECT user_id, name FROM user_table")

            columns = cur.fetchall()

            return columns
