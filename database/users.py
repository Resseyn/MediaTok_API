import time
from datetime import datetime
import json

from database import postgres
from scripts.date import get_month_name


class User:
    def __init__(self, user_id, login, password, name, surname, activity, created_at, creator_id):
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
    cursor = connection.cursor()

    @classmethod
    def create_user_table(cls):
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
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_user(cls, login, password, name, surname):
        insert_query = ("INSERT INTO users (login, password, name, surname, activity, created_at) "
                        "VALUES (%s, %s, %s, %s, True, %s) RETURNING user_id")
        try:
            cls.cursor.execute(insert_query, (login, password, name, surname,
                                              time.time(),))
        except:
            cls.connection.commit()
            return None
        user_id = cls.cursor.fetchone()[0]
        cls.connection.commit()
        return user_id

    @classmethod
    def get_user_by_id(cls, user_id):
        select_query = "SELECT * FROM users WHERE user_id = %s"
        cls.cursor.execute(select_query, (user_id,))
        user_data = cls.cursor.fetchone()
        user = User(*user_data)
        return user

    @classmethod
    def get_user_by_auth(cls, login, password):
        select_query = "SELECT * FROM users WHERE login = %s AND password = %s"
        cls.cursor.execute(select_query, (login, password))
        user_data = cls.cursor.fetchone()
        if user_data is None:
            return None
        user = User(*user_data)
        return user

    @classmethod
    def show_users(cls):
        select_query = "SELECT * FROM users"
        cls.cursor.execute(select_query)
        users_data = cls.cursor.fetchall()
        users = []
        for user_data in users_data:
            users.append(User(*user_data).__dict__)
        return users

    @classmethod
    def change_user_activity(cls, user_id):
        select_query = "SELECT * FROM users WHERE user_id = %s"
        cls.cursor.execute(select_query, (user_id,))
        user_data = cls.cursor.fetchone()
        update_query = "UPDATE users SET activity = %s WHERE user_id = %s"
        cls.cursor.execute(update_query, (not (user_data[5]), (user_id,)))
        cls.connection.commit()
        return not (user_data[5])

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()


# Пример использования
UserDB.create_user_table()
UserDB.add_user("bestseller2024", "DhdhJldkd@&jejsjs@wiwiw196373.ieie",
                "bestseller2024", "bestseller2024")
UserDB.add_user("zenki", "54T44f@f##@555gf3clw[e12!!!46kfgs$33$33",
                "zenki", "zenki")
UserDB.add_user("Dark_Counter", "Jeududu&dhshdh@eieieiei1938373@dbdhdh",
                "Dark_Counter", "Dark_Counter")
