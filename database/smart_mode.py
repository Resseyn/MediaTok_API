import json
from datetime import datetime

from database import postgres


class SmartMode:
    def __init__(self, toggle, sleep_time, promotion_time_and_percentage, update_time, creator_id):
        self.toggle = toggle
        self.sleep_time = sleep_time
        self.promotion_time_and_percentage = promotion_time_and_percentage
        self.update_time = update_time
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
                sleep_time TEXT NOT NULL,
                promotion_time_and_percentage TEXT,
                update_time BIGINT NOT NULL,
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
    def change_update_time(cls):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT update_time,sleep_time FROM smart_mode WHERE toggle = %s"
            cursor.execute(select_query, (True,))
            fetch_data = cursor.fetchone()
            if fetch_data is None:
                return "Smart_mode is off"
            user_data = fetch_data
            update_query = "UPDATE smart_mode SET update_time = %s WHERE toggle = %s"
            new_update_time = int(user_data[0]) + 1 if int(user_data[0]) < 24 else 0
            cursor.execute(update_query, (new_update_time, True,))
            cls.connection.commit()
            cursor.close()
            return "Changed update time (smart_mode) to ", new_update_time

    @classmethod
    def add_property(cls, toggle, sleep_time, promotion_time_and_percentage, creator_id):

        sleep_time += "000"

        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            cursor.execute(select_query, (creator_id,))
            server_data = cursor.fetchone()
            if server_data is not None:
                SmartModeDB.change_smart_mode_property(toggle, sleep_time, promotion_time_and_percentage, creator_id)
                return SmartMode(toggle, sleep_time, promotion_time_and_percentage, datetime.now().hour,
                                 creator_id).__dict__
            insert_query = (
                "INSERT INTO smart_mode (toggle,sleep_time,promotion_time_and_percentage,update_time,creator_id) "
                "VALUES (%s, %s, %s, %s, %s) RETURNING creator_id")
            try:
                cursor.execute(insert_query,
                               (toggle, sleep_time, promotion_time_and_percentage, datetime.now().hour, creator_id,))
                cls.connection.commit()
                cursor.close()
                return SmartMode(toggle, sleep_time, promotion_time_and_percentage, datetime.now().hour,
                                 creator_id).__dict__
            except Exception as e:
                print(f"Error adding property: {e}")
                cls.connection.rollback()
                cursor.close()
                return "0xdb"

    @classmethod
    def show_smart_mode(cls, creator_id):
        with cls.connection.cursor() as cursor:
            select_query = "SELECT * FROM smart_mode WHERE creator_id = %s"
            try:
                cursor.execute(select_query, (creator_id,))
                smart_mode_data = cursor.fetchone()
                return SmartMode(*smart_mode_data).__dict__ if smart_mode_data else "0xst"
            except Exception as e:
                print(f"Error showing smart_modes: {e}")
                cls.connection.rollback()
                return "0xdb"

    @classmethod
    def change_smart_mode_property(cls, toggle, sleep_time, promotion_time_and_percentage, creator_id):
        with cls.connection.cursor() as cursor:
            try:
                update_query = """
                UPDATE smart_mode 
                SET toggle = %s, 
                    sleep_time = %s, 
                    promotion_time_and_percentage = %s, 
                    update_time = %s
                WHERE creator_id = %s
                """
                cursor.execute(update_query,
                               (toggle, sleep_time, promotion_time_and_percentage, datetime.now().hour, creator_id))
                cls.connection.commit()
                smart_mode = SmartMode(toggle, sleep_time, promotion_time_and_percentage, datetime.now().hour,
                                       creator_id)
                return smart_mode.__dict__
            except Exception as e:
                print(f"Error changing smart_mode property: {e}")
                cls.connection.rollback()
                return "0xdb"

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# async def auto_change_sleep_time():
#     while True:
#         if datetime.now().minute <= 1:
#             print(SmartModeDB.change_update_time())
#         await asyncio.sleep(60) TODO: убийца богов


# Пример использования.
SmartModeDB.create_smart_mode_table()
