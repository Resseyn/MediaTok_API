import time
from datetime import datetime
import json

from database import postgres
from scripts.date import get_month_name

#TODO: как и с link тупо есть таблица и класс (тут таблица мб неправильная завтра спрошу)
class SiteTime:
    def __init__(self, time_id, emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min,number_of_transitions_max,
                 creator_id):
        self.time_id = time_id
        self.emulation_of_inactivity_min = emulation_of_inactivity_min
        self.emulation_of_inactivity_max = emulation_of_inactivity_max
        self.make_transitions = make_transitions
        self.emulation_of_inactivity_between_articles_min = emulation_of_inactivity_between_articles_min
        self.emulation_of_inactivity_between_articles_max = emulation_of_inactivity_between_articles_max
        self.number_of_transitions_min = number_of_transitions_min
        self.number_of_transitions_max = number_of_transitions_max
        self.creator_id = creator_id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class SiteTimeDB():
    connection = postgres.conn
    cursor = connection.cursor()

    @classmethod
    def create_user_table(cls):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS site_time (
            time_id SERIAL PRIMARY KEY,
            emulation_of_inactivity_min INTEGER NOT NULL,
            emulation_of_inactivity_max INTEGER NOT NULL,
            make_transitions BOOLEAN NOT NULL,
            emulation_of_inactivity_between_articles_min INTEGER NOT NULL,
            emulation_of_inactivity_between_articles_min INTEGER NOT NULL,
            number_of_transitions_min INTEGER NOT NULL,
            number_of_transitions_max INTEGER NOT NULL,
            creator_id INTEGER NOT NULL
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_user(cls, login, password, name, surname, creator_id):
        insert_query = ("INSERT INTO users (login, password, name, surname, activity, created_at, creator_id) "
                        "VALUES (%s, %s, %s, %s, True, %s, %s) RETURNING user_id")
        cls.cursor.execute(insert_query, (login, password, name, surname,
                                          time.time(),
                                          creator_id,))
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
UserDB.create_user_table()