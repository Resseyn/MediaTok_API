import json

import psycopg2

from database import postgres
from database.postgres import SingletonMeta


class User:
    def __init__(self, user_id, name, password, activity=True):
        self.user_id = user_id
        self.name = name
        self.password = password
        self.activity = activity
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class UserDB(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = postgres.conn
        self.cursor = self.connection.cursor()

    def create_user_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            activity BOOLEAN NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_user(self, name, password):
        insert_query = "INSERT INTO users (name, password) VALUES (%s, %s) RETURNING user_id"
        self.cursor.execute(insert_query, (name, password))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return user_id

    def get_user_by_id(self, user_id):
        select_query = "SELECT * FROM users WHERE user_id = %s"
        self.cursor.execute(select_query, (user_id,))
        user_data = self.cursor.fetchone()
        if user_data:
            return User(user_data[0], user_data[1], user_data[2], user_data[3])
        return None

    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# Пример использования
user_db = UserDB()
user_db.create_user_table()
# Добавление пользователя
new_user_id = user_db.add_user('John', 'password123')

# Получение пользователя по ID
user = user_db.get_user_by_id(new_user_id)
if user:
    print(f"User found: ID={user.user_id}, Name={user.name}, Password={user.password}, ACtivity= {user.activity}")
else:
    print("User not found")

#user_db.close_connection()
