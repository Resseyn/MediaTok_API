import json
import time
import psycopg2
from database import postgres


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
            cls.connection.rollback()
            cursor.close()

    @classmethod
    def add_server(cls, name, login_anyd, password_anyd, cpu, ram, storage, ip, activity, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO servers (name, login_anyd, password_anyd, cpu, ram, storage,ip, activity, to_a_specific_proxy, created_at, creator_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING server_id, name, login_anyd, password_anyd, cpu, ram, storage,ip, activity, to_a_specific_proxy, created_at, creator_id")
                cursor.execute(insert_query, (name, login_anyd, password_anyd, cpu, ram, storage, ip, activity, False,
                                              time.time(),
                                              creator_id,))
                server_data = cursor.fetchone()
                cls.connection.commit()
                return Server(*server_data).__dict__
        except psycopg2.Error as e:
            print("Ошибка add server(servers.py):", e)
            cls.connection.rollback()
            cursor.close()

    @classmethod
    def get_server_by_id(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                if server_data:
                    return Server(*server_data).__dict__
                return None
        except psycopg2.Error as e:
            cursor.close()
            cls.connection.rollback()
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
            cursor.close()
            cls.connection.rollback()
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
            cls.connection.rollback()
            print("Error changing server activity(servers.py):", e)
            cursor.close()

    @classmethod
    def change_proxy_flag(cls, server_id, flag):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, server_id)
                server_data = cursor.fetchone()
                if server_data:
                    update_query = "UPDATE servers SET to_a_specific_proxy = %s WHERE server_id = %s"
                    cursor.execute(update_query, (flag, server_id,))
                    cls.connection.commit()
                    return True
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error changing proxy flag (servers.py):",e)
            cursor.close()

    @classmethod
    def delete_server(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                delete_query = ("DELETE FROM servers WHERE server_id = %s")
                cursor.execute(delete_query, (server_id,))
                cls.connection.commit()
                return True
        except psycopg2.Error as e:
            print("Error deleting proxy:", e)
            cls.connection.rollback()
            return False

    @classmethod
    def change_server(cls, server_id, name, login_anyd, password_anyd, cpu, ram, storage, ip, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM servers WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                server_data = cursor.fetchone()
                if server_data:
                    update_query = """
                    UPDATE servers SET 
                    name = %s, 
                    login_anyd = %s, 
                    password_anyd = %s, 
                    cpu = %s, 
                    ram = %s, 
                    storage = %s,
                    ip = %s, 
                    activity = %s
                    WHERE server_id = %s;"""
                    cursor.execute(update_query, (
                    name, login_anyd, password_anyd, cpu, ram, storage, ip, server_data[8], server_id
                    ))
                    cls.connection.commit()
                    return Server(server_id, name, login_anyd, password_anyd,  cpu, ram, storage, ip,
                                  server_data[8], server_data[9], server_data[10], creator_id).__dict__
                return None
        except psycopg2.Error as e:
            print(f"Error changing link:", e)
            cls.connection.rollback()
    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
ServersDB.create_server_table()
