import json
import time
from datetime import datetime

from database import postgres
from scripts.date import get_month_name


class Search:
    def __init__(self, search_id, search_for, link, properties, list_seti, activity, created_at,creator_id, ):
        self.search_id = search_id
        self.search_for = search_for
        self.link = link
        self.properties = properties
        self.list_seti = list_seti
        self.activity = activity
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class SearchesDB:
    connection = postgres.conn

    @classmethod
    def create_searches_table(cls):
        cursor = cls.connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS searches (
            search_id SERIAL PRIMARY KEY,
            search_for VARCHAR(255) NOT NULL,
            link TEXT NOT NULL,
            properties TEXT NOT NULL,
            list_seti BOOLEAN NOT NULL,
            activity BOOLEAN NOT NULL,
            created_at BIGINT NOT NULL,
            creator_id INTEGER NOT NULL
        );
        """
        cursor.execute(create_table_query)
        cls.connection.commit()
        cursor.close()

    @classmethod
    def add_search(cls, search_for, link, properties, creator_id):
        cursor = cls.connection.cursor()
        insert_query = (
            "INSERT INTO searches (search_for, link, properties, activity, created_at,creator_id) "
            "VALUES (%s, %s, %s, %s,%s) RETURNING server_id")
        cls.cursor.execute(insert_query, (search_for, link, properties, True,
                                          time.time(),
                                          creator_id,))
        server_id = cursor.fetchone()[0]
        cls.connection.commit()
        cursor.close()
        return server_id

    @classmethod
    def get_server_by_id(cls, server_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM servers WHERE server_id = %s"
        cursor.execute(select_query, (server_id,))
        server_data = cursor.fetchone()
        server = Server(*server_data)
        cursor.close()
        return server

    @classmethod
    def show_servers(cls, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM servers WHERE creator_id = %s"
        cursor.execute(select_query, (creator_id,))
        servers_data = cursor.fetchall()
        servers = []
        for server_data in servers_data:
            servers.append(Server(*server_data).__dict__)
        cursor.close()
        return servers

    @classmethod
    def change_server_activity(cls, server_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM servers WHERE server_id = %s"
        cursor.execute(select_query, (server_id,))
        server_data = cls.cursor.fetchone()
        update_query = "UPDATE servers SET activity = %s WHERE server_id = %s"
        cursor.execute(update_query, (not (server_data[8]), (server_id,)))
        cls.connection.commit()
        cursor.close()
        return not (server_data[8])

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования
ServersDB.create_server_table()
