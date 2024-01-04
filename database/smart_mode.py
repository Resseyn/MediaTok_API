import json
import time
from datetime import datetime

from database import postgres
from scripts.date import get_month_name


class SmartMode:
    def __init__(self, toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id):
        self.toggle = toggle
        self.sleep_time = sleep_time
        self.promotion_time_and_percentage = promotion_time_and_percentage
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SmartModeDB:
    connection = postgres.conn

    @classmethod
    def create_smart_mode_table(cls):
        with cls.connection.cursor() as cursor:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS smart_mode (
                honorable_mention INTEGER NOT NULL PRIMARY KEY,
                smart_mode BOOLEAN NOT NULL,
                sleep_time INTEGER NOT NULL,
                promotion_time_and_percentage TEXT,
                created_at BIGINT NOT NULL,
                creator_id INTEGER NOT NULL
            );
            """
            try:
                cursor.execute(create_table_query)
                cls.connection.commit()
            except Exception as e:
                print(f"Error creating smart_mode table: {e}")
                cls.connection.rollback()

    @classmethod
    def add_property(cls, honorable_mention, toggle, sleep_time, promotion_time_and_percentage, creator_id):
        with cls.connection.cursor() as cursor:
            insert_query = (
                "INSERT INTO smart_mode (server_id,toggle,sleep_time,promotion_time_and_percentage,created_at,creator_id) "
                "VALUES (%s, %s, %s, %s, %s, %s) RETURNING server_id")
            try:
                cursor.execute(insert_query, (honorable_mention, toggle, sleep_time, promotion_time_and_percentage, time.time(), creator_id,))
                honorable_mention = cursor.fetchone()[0]
                cls.connection.commit()
                return SmartMode(honorable_mention, toggle, sleep_time,promotion_time_and_percentage, creator_id).__dict__
            except Exception as e:
                print(f"Error adding property: {e}")
                cls.connection.rollback()

    @classmethod
    def get_smart_mode_by_server_id(cls, server_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE server_id = %s"
            try:
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                smart_mode = SmartMode(*server_data).__dict__
                return smart_mode
            except Exception as e:
                print(f"Error getting smart_mode by server_id: {e}")
                cls.connection.rollback()

    @classmethod
    def show_smart_modes(cls, creator_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            try:
                cursor.execute(select_query, (creator_id,))
                smart_modes_data = cursor.fetchall()
                smart_modes = []
                for smart_mode in smart_modes_data:
                    smart_modes.append(SmartMode(*smart_mode).__dict__)
                return smart_modes[0]
            except Exception as e:
                print(f"Error showing smart_modes: {e}")
                cls.connection.rollback()

    @classmethod
    def change_smart_mode_property(cls, server_id, toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE server_id = %s"
            try:
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
                smart_mode = SmartMode(server_id, sleep_time, promotion_time_and_percentage, created_at, creator_id)
                return smart_mode.__dict__
            except Exception as e:
                print(f"Error changing smart_mode property: {e}")
                cls.connection.rollback()

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
SmartModeDB.create_smart_mode_table()
