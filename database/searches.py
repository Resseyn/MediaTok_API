import json
import time
from datetime import datetime

import psycopg2

from database import postgres
from database.servers import ServersDB
from scripts.date import get_month_name

#TODO: erorr exceptions
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
        try:
            cursor.execute(create_table_query)
            cls.connection.commit()
        except Exception as e:
            print(f"Error creating searches table: {e}")
            cls.connection.rollback()
        cursor.close()

    @classmethod
    def add_search(cls, search_for, link, properties, creator_id):
        cursor = cls.connection.cursor()
        insert_query = (
            "INSERT INTO searches (search_for, link, properties, list_seti, activity, created_at,creator_id) "
            "VALUES (%s, %s, %s, %s,%s, %s, %s) RETURNING search_id")
        cursor.execute(insert_query, (search_for, link, properties, (False if properties == "" else True), True,
                                          time.time(),
                                          creator_id,))
        server_id = cursor.fetchone()[0]
        cls.connection.commit()
        cursor.close()
        return server_id

    @classmethod
    def get_search_by_id(cls, search_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM searches WHERE search_id = %s"
        cursor.execute(select_query, (search_id,))
        search_data = cursor.fetchone()
        search = Search(*search_data).__dict__
        cursor.close()
        return search

    @classmethod
    def show_searches(cls, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM searches WHERE creator_id = %s"
        cursor.execute(select_query, (creator_id,))
        searches_data = cursor.fetchall()
        searches = []
        for search_data in searches_data:
            searches.append(Search(*search_data).__dict__)
        cursor.close()
        return searches

    @classmethod
    def change_search_activity(cls, search_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM searches WHERE search_id = %s"
        cursor.execute(select_query, (search_id,))
        search_data = cursor.fetchone()
        update_query = "UPDATE searches SET activity = %s WHERE search_id = %s"
        cursor.execute(update_query, (not (search_data[5]), (search_id,)))
        cls.connection.commit()
        cursor.close()
        return not (search_data[5])

    @classmethod
    def delete_search(cls, search_id):
        try:
            with cls.connection.cursor() as cursor:
                delete_query = ("DELETE FROM searches WHERE search_id = %s")
                cursor.execute(delete_query, (search_id,))
                return True
        except psycopg2.Error as e:
            print("Error deleting proxy:", e)
            cls.connection.rollback()
            return False
    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
SearchesDB.create_searches_table()
