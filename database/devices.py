import json
import psycopg2
from database import postgres


class Device:
    def __init__(self, record_id,phone,desktop,tablet,creator_id):
        self.record_id = record_id
        self.phone = phone
        self.desktop = desktop
        self.tablet = tablet
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class DevicesDB:
    connection = postgres.conn

    @classmethod
    def create_devices_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS devices (
                    record_id SERIAL PRIMARY KEY,
                    phone INTEGER NOT NULL,
                    desktop INTEGER NOT NULL,
                    tablet INTEGER NOT NULL,
                    creator_id INTEGER NOT NULL
                );
            """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print(f"Error creating devices table: {e}")

    @classmethod
    def add_device(cls, phone,desktop,tablet,creator_id):
        if int(phone) + int(desktop) + int(tablet) != 100:
            return None
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO devices (phone,desktop,tablet,creator_id) "
                    "VALUES (%s, %s, %s,%s) RETURNING record_id"
                )
                cursor.execute(insert_query, (phone,int(phone) + int(desktop), 100,creator_id)
                               )
                record_id = cursor.fetchone()[0]
                cls.connection.commit()
                return Device(record_id,phone,int(phone) + int(desktop), 100,creator_id).__dict__
        except psycopg2.Error as e:
            print(f"Error adding device: {e}")
            return None

    @classmethod
    def change_device(cls,record_id,phone,desktop,tablet):
        if int(phone) + int(desktop) + int(tablet) != 100:
            return None
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM devices WHERE record_id = %s"
                cursor.execute(select_query, (record_id))
                device_data = cursor.fetchone()
                if device_data:
                    # я хуй знает как тут сделать прием по 20-50-30 или 20-70-100 (сделал 20-50-30)
                    # TODO: Разобраться с приемом процентов
                    update_query = '''UPDATE devices 
                SET phone = %s, 
                    desktop = %s, 
                    tablet = %s
                WHERE record_id = %s
                RETURNING creator_id'''
                    cursor.execute(update_query, (phone,int(phone) + int(desktop), 100,record_id))
                    creator_id = cursor.fetchone()[0]
                    cls.connection.commit()
                    return Device(record_id, phone,int(phone) + int(desktop), 100 ,creator_id).__dict__
                return None
        except psycopg2.Error as e:
            cls.connection.rollback()
            print(f"Error changing device:",e)

    @classmethod
    def show_devices(cls, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM devices WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                devices_data = cursor.fetchall()
                devices = [Device(*device_data).__dict__ for device_data in devices_data]
                return devices
        except psycopg2.Error as e:
            cls.connection.rollback()
            print(f"Error showing devices: {e}")

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
DevicesDB.create_devices_table()
