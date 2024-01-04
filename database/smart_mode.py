import json
import time
from datetime import datetime

from database import postgres
from scripts.date import get_month_name


class SmartMode:
    def __init__(self, toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id):
        self.toggle = toggle
        self.sleep_time = sleep_time
        self.promotion_time_and_precentage = promotion_time_and_percentage
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SmartModeDB:
    connection = postgres.conn

    @classmethod
    def create_smart_mode_table(cls):
        cursor = cls.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS smart_mode (
            server_id INTEGER NOT NULL PRIMARY KEY,
            smart_mode BOOLEAN NOT NULL,
            sleep_time INTEGER NOT NULL,
            promotion_time_and_percentage TEXT,
            created_at BIGINT NOT NULL,
            creator_id INTEGER NOT NULL
        );
        """
        cursor.execute(create_table_query)
        cursor.close()
        cls.connection.commit()

    @classmethod
    def add_operation(cls, server_id, toggle, sleep_time, promotion_time_and_percentage, creator_id):
        cursor = cls.connection.cursor()
        insert_query = (
            "INSERT INTO smart_mode (server_id,toggle,sleep_time,promotion_time_and_percentage,created_at,creator_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING server_id")
        cursor.execute(insert_query, (server_id, toggle, sleep_time, promotion_time_and_percentage, time.time(), creator_id,))
        server_id = cursor.fetchone()[0]
        cls.connection.commit()
        cursor.close()
        return server_id

    @classmethod
    def get_smart_mode_by_server_id(cls, server_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM smart_mode WHERE server_id = %s"
        cursor.execute(select_query, (server_id,))
        server_data = cursor.fetchone()
        smart_mode = SmartMode(*server_data)
        cursor.close()
        return smart_mode

    @classmethod
    def show_smart_modes(cls, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
        cursor.execute(select_query, (creator_id,))
        smart_modes_data = cursor.fetchall()
        smart_modes = []
        for smart_mode in smart_modes_data:
            smart_modes.append(SmartMode(*smart_mode).__dict__)
        cursor.close()
        return smart_modes

    @classmethod
    def change_smart_mode(cls, server_id, toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM smart_mode WHERE server_id = %s"
        cursor.execute(select_query, (server_id,))
        server_data = cursor.fetchone()
        update_query = """
        UPDATE smart_mode 
        SET smart_mode = %s, 
            sleep_time = %s, 
            promotion_time_and_precentage = %s, 
            created_at = %s, 
            creator_id = %s 
        WHERE server_id = %s
        """
        cursor.execute(update_query,
                       (toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id, server_id))
        cls.connection.commit()
        cursor.close()
        smart_mode = SmartMode(server_id, sleep_time, promotion_time_and_percentage, created_at, creator_id)
        return smart_mode   # извините надеюсь тебе не придется ебаться с тем что это отличается от всех остальных
        # таких штук

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования
SmartModeDB.create_smart_mode_table()
