import json
import time
from datetime import datetime
import psycopg2
from database import postgres
from scripts.date import get_month_name

class Server:
    def __init__(self, server_id, name, login_anyd, password_anyd, cpu, ram, storage, ip, activity, to_a_specific_proxy,
                 created_at,
                 creator_id, ):
        self.server_id = server_id
        self.name = name
        self.login_anyd = login_anyd
        self.password_anyd = password_anyd
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.ip = ip
        self.activity = activity
        self.to_a_specific_proxy = to_a_specific_proxy
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class ServersDB:
    connection = postgres.conn

    @classmethod
    def create_server_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS servers (
                    server_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    login_anyd VARCHAR(255) NOT NULL,
                    password_anyd VARCHAR(255) NOT NULL,
                    cpu VARCHAR(255) NOT NULL,
                    ram VARCHAR(255) NOT NULL,
                    storage VARCHAR(255) NOT NULL,
                    ip VARCHAR(255) NOT NULL,
                    activity BOOLEAN NOT NULL,
                    to_a_specific_proxy BOOLEAN NOT NULL,
                    created_at BIGINT NOT NULL,
                    creator_id INTEGER NOT NULL
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error creating server table(servers.py):", e)

    @classmethod
    def add_server(cls, name, login_anyd, password_anyd, cpu, ram, storage, ip, activity, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO servers (name, login_anyd, password_anyd, cpu, ram, storage,ip, activity, to_a_specific_proxy, created_at, creator_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING server_id")
                cursor.execute(insert_query, (name, login_anyd, password_anyd, cpu, ram, storage, ip, activity, False,
                                              time.time(),
                                              creator_id,))
                server_id = cursor.fetchone()[0]
                cls.connection.commit()
                return server_id
        except psycopg2.Error as e:
            print("Ошибка add server(servers.py):", e)

    @classmethod
    def get_server_by_id(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                if server_data:
                    return Server(*server_data)
                return None
        except psycopg2.Error as e:
            print("Error getting server by ID(servers.py):", e)

    @classmethod
    def show_servers(cls, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                servers_data = cursor.fetchall()
                servers = [Server(*server_data).__dict__ for server_data in servers_data]
                return servers
        except psycopg2.Error as e:
            print("Error showing servers(servers.py):", e)

    @classmethod
    def change_server_activity(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                if server_data:
                    update_query = "UPDATE servers SET activity = %s WHERE server_id = %s"
                    cursor.execute(update_query, (not server_data[8], server_id,))
                    cls.connection.commit()
                    return not server_data[8]
                return None
        except psycopg2.Error as e:
            print("Error changing server activity(servers.py):", e)

    @classmethod
    def change_proxy_flag(cls,server_id,flag):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, server_id)
                server_data = cursor.fetchone()
                if server_data:
                    update_query = "UPDATE servers SET to_a_specific_proxy = %s WHERE server_id = %s"
                    cursor.execute(update_query, flag,server_id)
                    cls.connection.commit()
                    return True
        except psycopg2.Error as e:
            print("Error changing proxy flag (servers.py):",e)


    @classmethod
    def close_connection(cls):
        cls.connection.close()

# Пример использования
ServersDB.create_server_table()
