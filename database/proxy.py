import json

import psycopg2

from database import postgres
from database.servers import ServersDB


class Proxy:
    def __init__(self, proxy_id, server_id, address, status, creator_id):
        self.proxy_id = proxy_id
        self.server_id = server_id
        self.address = address
        self.status = status
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class ProxyDB:
    connection = postgres.conn

    @classmethod
    def create_proxy_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS proxy (
                    proxy_id INT PRIMARY KEY,
                    server_id INT NOT NULL,
                    address TEXT NOT NULL,
                    status BOOLEAN NOT NULL,
                    creator_id INTEGER NOT NULL
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error creating proxy table(proxy.py):", e)

    @classmethod
    def add_proxy(cls, server_id, address, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO proxy (server_id, address, status, creator_id) "
                    "VALUES (%s, %s, %s, %s) RETURNING proxy_id"
                )
                cursor.execute(insert_query, (server_id, address, True, creator_id))
                proxy_id = cursor.fetchone()[0]
                cls.connection.commit()
                ServersDB.change_proxy_flag(server_id, True)
                return proxy_id
        except psycopg2.Error as e:
            print("Error adding proxy(proxy.py):", e)
            return None

    @classmethod
    def delete_proxy(cls, proxy_id):
        try:
            with cls.connection.cursor() as cursor:
                delete_query = ("DELETE FROM proxy WHERE proxy_id = %s RETURNING server_id")
                cursor.execute(delete_query, (proxy_id,))
                server_id = cursor.fetchone()[0]

                check_query = ("SELECT * FROM proxy WHERE server_id = %s")
                cursor.execute(check_query, (server_id,))

                current_server = cursor.fetchone()
                was_last_proxy = sum([1 for i in cursor.fetchall()]) > 0

                if was_last_proxy:
                    ServersDB.change_proxy_flag(server_id, False)
                return True
        except psycopg2.Error as e:
            print("Error deleting proxy:", e)
            return False

    @classmethod
    def get_proxy_by_server_id(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                proxy_data = cursor.fetchone()
                if proxy_data:
                    return Proxy(*proxy_data).__dict__
                return None
        except psycopg2.Error as e:
            print("Error getting proxy by ID(proxy.py):", e)
            return None

    @classmethod
    def get_proxy_by_proxy_id(cls, proxy_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE proxy_id = %s"
                cursor.execute(select_query, (proxy_id,))
                proxy_data = cursor.fetchone()
                if proxy_data:
                    return Proxy(*proxy_data)
                return None
        except psycopg2.Error as e:
            print("Error getting proxy by ID(proxy.py):", e)
            return None

    @classmethod
    def show_proxies(cls, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM proxy WHERE creator_id = %s"
        cursor.execute(select_query, (creator_id,))
        servers_data = cursor.fetchall()
        cursor.close()
        servers = []
        for server_data in servers_data:
            servers.append(Server(*server_data).__dict__)
        cursor.close()
        return servers

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования
ProxyDB.create_proxy_table()
