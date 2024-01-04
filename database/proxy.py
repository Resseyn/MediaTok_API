import json
import time
from datetime import datetime

from database import postgres
from database.servers import Server
from scripts.date import get_month_name


class Proxy:
    def __init__(self, server_id, proxies):
        self.server_id = server_id
        self.proxies = proxies


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
            proxy_list TEXT NOT NULL
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_server(cls, server_id, proxies):
        insert_query = (
            "INSERT INTO proxy (server_id,proxies) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING server_id")
        cls.cursor.execute(insert_query, (server_id, proxies))
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
    def show_servers(cls):
        select_query = "SELECT * FROM proxy"
        cls.cursor.execute(select_query)
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
