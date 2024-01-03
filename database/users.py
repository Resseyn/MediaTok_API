import json

from database import postgres


class User:
    def __init__(self, user_id, login, password, name, surname,  creator_id, activity=True):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.name = name
        self.surname = surname
        self.activity = activity
        self.creator_id = creator_id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class UserDB():
    connection = postgres.conn
    cursor = connection.cursor()

    @classmethod
    def create_user_table(cls):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL,
            name VARCHAR(255) NOT NULL,
            surname VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            activity BOOLEAN NOT NULL,
            creator_id INTEGER NOT NULL
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_user(cls, login, password, name, surname, creator_id):
        insert_query = ("INSERT INTO users (login, password, name, surname, activity, creator_id) "
                        "VALUES (%s, %s, %s, %s, True, %s) RETURNING user_id")
        cls.cursor.execute(insert_query, (login, password, name, surname, creator_id,))
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
    def show_users(cls, client_id):
        select_query = "SELECT * FROM users WHERE creator_id = %s"
        cls.cursor.execute(select_query, (client_id,))
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
        cls.cursor.execute(update_query, (not(user_data[5]), (user_id,)))
        cls.connection.commit()
        return not(user_data[5])

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()

# Пример использования
# user_db.create_user_table()
# # Добавление пользователя
# new_user_id = user_db.add_user('login', 'password123', "John", "Doe", "1")
#
# # Получение пользователя по ID
# user = user_db.get_user_by_id(new_user_id)
# if user:
#     print(f"User found: {user}")
# else:
#     print("User not found")
#
# #user_db.close_connection()
