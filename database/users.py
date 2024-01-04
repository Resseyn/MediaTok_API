import time
import json

from database import postgres


class User:
    def __init__(self, user_id, login, password, name, surname, activity, created_at):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.activity = activity
        self.created_at = created_at

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class UserDB:
    connection = postgres.conn

    @classmethod
    def create_user_table(cls):
        cursor = cls.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL UNIQUE,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            activity BOOLEAN NOT NULL,
            created_at BIGINT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        cls.connection.commit()
        cursor.close()

    @classmethod
    def add_user(cls, login, password, name, surname):
        cursor = cls.connection.cursor()
        insert_query = ("INSERT INTO users (login, password, name, surname, activity, created_at) "
                        "VALUES (%s, %s, %s, %s, True, %s) RETURNING user_id")
        try:
            cursor.execute(insert_query, (login, password, name, surname,
                                          time.time(),))
        except:
            cls.connection.commit()
            return None
        # TODO: пайтон эксепшен
        user_id = cursor.fetchone()[0]
        cls.connection.commit()
        cursor.close()
        return user_id

    @classmethod
    def get_user_by_id(cls, user_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        user_data = cursor.fetchone()
        user = User(*user_data)
        cursor.close()
        return user

    @classmethod
    def get_user_by_auth(cls, login, password):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM users WHERE login = %s AND password = %s"
        cursor.execute(select_query, (login, password))
        user_data = cursor.fetchone()
        if user_data is None:
            return None
        user = User(*user_data)
        cursor.close()
        return user

    @classmethod
    def show_users(cls):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM users"
        cursor.execute(select_query)
        users_data = cursor.fetchall()
        users = []
        for user_data in users_data:
            users.append(User(*user_data).__dict__)
        cursor.close()
        return users

    @classmethod
    def change_user_activity(cls, user_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(select_query, (user_id,))
        user_data = cursor.fetchone()
        update_query = "UPDATE users SET activity = %s WHERE user_id = %s"
        cursor.execute(update_query, (not (user_data[5]), (user_id,)))
        cls.connection.commit()
        cursor.close()
        return not (user_data[5])

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования
UserDB.create_user_table()
UserDB.add_user("bestseller2024", "DhdhJldkd@&jejsjs@wiwiw196373.ieie",
                "bestseller2024", "bestseller2024")
UserDB.add_user("zenki", "54T44f@f##@555gf3clw[e12!!!46kfgs$33$33",
                "zenki", "zenki")
UserDB.add_user("Dark_Counter", "Jeududu&dhshdh@eieieiei1938373@dbdhdh",
                "Dark_Counter", "Dark_Counter")
