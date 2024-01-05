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
                toggle BOOLEAN NOT NULL,
                sleep_time INTEGER NOT NULL,
                promotion_time_and_percentage TEXT,
                created_at BIGINT NOT NULL,
                creator_id INTEGER PRIMARY KEY NOT NULL
            );
            """
            try:
                cursor.execute(create_table_query)
                cls.connection.commit()
            except Exception as e:
                print(f"Error creating smart_mode table: {e}")
                cls.connection.rollback()
            cursor.close()

    @classmethod
    def add_property(cls, toggle, sleep_time, promotion_time_and_percentage, creator_id):

        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            cursor.execute(select_query, (creator_id,))
            server_data = cursor.fetchone()
            if server_data is not None:
                SmartModeDB.change_smart_mode_property(toggle, sleep_time, promotion_time_and_percentage, time.time(), creator_id)
                return SmartMode(toggle, sleep_time, promotion_time_and_percentage, time.time(), creator_id).__dict__
            #TODO: это если уже есть запись в бд, вроде должно работать
            insert_query = (
                "INSERT INTO smart_mode (toggle,sleep_time,promotion_time_and_percentage,created_at,creator_id) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING creator_id")
            try:
                cursor.execute(insert_query, (toggle, sleep_time, promotion_time_and_percentage, time.time(), creator_id,))
                cls.connection.commit()
                cursor.close()
                return SmartMode(toggle, sleep_time, promotion_time_and_percentage,  time.time(),creator_id).__dict__
            except Exception as e:
                print(f"Error adding property: {e}")
                cls.connection.rollback()
                cursor.close()

    @classmethod
    def get_smart_mode_by_server_id(cls, server_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            try:
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                smart_mode = SmartMode(*server_data).__dict__
                return smart_mode
            except Exception as e:
                print(f"Error getting smart_mode by server_id: {e}")
                cls.connection.rollback()

    @classmethod
    def show_smart_mode(cls, creator_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            try:
                cursor.execute(select_query, (creator_id,))
                smart_mode_data = cursor.fetchone()
                return SmartMode(*smart_mode_data).__dict__
            except Exception as e:
                print(f"Error showing smart_modes: {e}")
                cls.connection.rollback()

    @classmethod
    def change_smart_mode_property(cls, toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id):
        with cls.connection.cursor() as cursor:
            try:
                update_query = """
                UPDATE smart_mode 
                SET toggle = %s, 
                    sleep_time = %s, 
                    promotion_time_and_percentage = %s, 
                    created_at = %s
                WHERE creator_id = %s
                """
                cursor.execute(update_query,
                               (toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id))
                cls.connection.commit()
                smart_mode = SmartMode(toggle, sleep_time, promotion_time_and_percentage, created_at, creator_id)
                return smart_mode.__dict__
            except Exception as e:
                print(f"Error changing smart_mode property: {e}")
                cls.connection.rollback()

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
SmartModeDB.create_smart_mode_table()
