import json
import time
from datetime import datetime

from database import postgres
from database.servers import Server
from scripts.date import get_month_name


class Proxy:
    def __init__(self, server_id, proxies, creator_id):
        self.server_id = server_id
        self.proxies = proxies
        self.creator_id = creator_id


    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class ProxyDB:
    connection = postgres.conn
    cursor = connection.cursor()

    @classmethod
    def create_proxy_table(cls):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS proxy (
            server_id INT PRIMARY KEY,
            proxy_list TEXT NOT NULL,
            creator_id INTEGER NOT NULL
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_proxy(cls, server_id, proxies, creator_id):
        insert_query = (
            "INSERT INTO proxy (server_id,proxies, creator_id) "
            "VALUES (%s, %s, %s) RETURNING server_id")
        cls.cursor.execute(insert_query, (server_id, proxies, creator_id))
        server_id = cls.cursor.fetchone()[0]
        cls.connection.commit()
        return server_id

    @classmethod
    def get_proxy_by_id(cls, server_id):
        select_query = "SELECT * FROM proxy WHERE server_id = %s"
        cls.cursor.execute(select_query, (server_id,))
        proxy_data = cls.cursor.fetchone()
        proxy = Proxy(*proxy_data)
        return proxy

    @classmethod
    def show_proxies(cls, creator_id):
        select_query = "SELECT * FROM proxy WHERE creator_id = %s"
        cls.cursor.execute(select_query, (creator_id,))
        servers_data = cls.cursor.fetchall()
        cls.cursor.close()
        servers = []
        for server_data in servers_data:
            servers.append(Server(*server_data).__dict__)
        return servers

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()


# Пример использования
ProxyDB.create_proxy_table()
