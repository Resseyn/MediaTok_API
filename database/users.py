import time
import json
import psycopg2
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
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class UserDB:
    connection = postgres.conn

    @classmethod
    def create_user_table(cls):
        try:
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
        except psycopg2.Error as e:
            print("Error creating user table:", e)
        finally:
            if cursor:
                cursor.close()

    @classmethod
    def add_user(cls, login, password, name, surname):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = ("INSERT INTO users (login, password, name, surname, activity, created_at) "
                                "VALUES (%s, %s, %s, %s, True, %s) RETURNING user_id")
                cursor.execute(insert_query, (login, password, name, surname, time.time()))
                user_id = cursor.fetchone()[0]
                cls.connection.commit()
                return user_id
        except psycopg2.Error as e:
            print("Error adding user:", e)
            return None

    @classmethod
    def get_user_by_id(cls, user_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM users WHERE user_id = %s"
                cursor.execute(select_query, (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    return User(*user_data)
                return None
        except psycopg2.Error as e:
            print("Error getting user by ID:", e)

    @classmethod
    def get_user_by_auth(cls, login, password):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM users WHERE login = %s AND password = %s"
                cursor.execute(select_query, (login, password))
                user_data = cursor.fetchone()
                if user_data:
                    return User(*user_data).__dict__
                return None
        except psycopg2.Error as e:
            print("Error getting user by authentication:", e)

    @classmethod
    def show_users(cls):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM users"
                cursor.execute(select_query)
                users_data = cursor.fetchall()
                users = [User(*user_data).__dict__ for user_data in users_data]
                return users
        except psycopg2.Error as e:
            print("Error showing users:", e)

    @classmethod
    def change_user_activity(cls, user_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM users WHERE user_id = %s"
                cursor.execute(select_query, (user_id,))
                user_data = cursor.fetchone()
                if user_data:
                    update_query = "UPDATE users SET activity = %s WHERE user_id = %s"
                    cursor.execute(update_query, (not user_data[5], user_id,))
                    cls.connection.commit()
                    return not user_data[5]
                return None
        except psycopg2.Error as e:
            print("Error changing user activity:", e)

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
