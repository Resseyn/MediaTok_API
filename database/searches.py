import json
import time

import psycopg2

from database import postgres


# TODO: error exceptions
class Search:
    def __init__(self, search_id, search_for, link, properties, list_seti, activity, created_at, creator_id):
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
        with cls.connection.cursor() as cursor:
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

    @classmethod
    def add_search(cls, search_for, link, properties, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO searches (search_for, link, properties, list_seti, activity, created_at,creator_id) "
                    "VALUES (%s, %s, %s, %s,%s, %s, %s) RETURNING search_id")
                cursor.execute(insert_query, (search_for, link, properties, (False if properties == "" else True), True,
                                              time.time(),
                                              creator_id,))
                server_id = cursor.fetchone()[0]
                cls.connection.commit()
                return server_id
        except psycopg2.Error as e:
            print(f"Error adding search: {e}")
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def get_search_by_id(cls, search_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM searches WHERE search_id = %s"
                cursor.execute(select_query, (search_id,))
                search_data = cursor.fetchone()
                if search_data:
                    search = Search(*search_data).__dict__
                    return search
                else:
                    return "0xdb"
        except psycopg2.Error as e:
            print(f"Error getting search by ID: {e}")
            return "0xdb"

    @classmethod
    def show_searches(cls, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM searches WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                searches_data = cursor.fetchall()
                searches = [Search(*search_data).__dict__ for search_data in searches_data]
                return searches
        except psycopg2.Error as e:
            print(f"Error showing searches: {e}")
            return "0xdb"

    @classmethod
    def change_search_activity(cls, search_id,creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM searches WHERE search_id = %s"
                cursor.execute(select_query, (search_id,))
                search_data = cursor.fetchone()
                if search_data[-1] == creator_id:
                    update_query = "UPDATE searches SET activity = %s WHERE search_id = %s"
                    cursor.execute(update_query, (not search_data[5], search_id))
                    cls.connection.commit()
                    return not search_data[5]
                else:
                    return "0xperm"
        except psycopg2.Error as e:
            print(f"Error changing search activity: {e}")
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def delete_search(cls, search_id,creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT creator_id FROM searches WHERE search_id = %s"
                cursor.execute(select_query, (search_id,))
                fetch_data = cursor.fetchone()
                if fetch_data is None:
                    return "0xdb"
                creator_id_from_db = fetch_data[0]
                if creator_id_from_db != creator_id:
                    return "0xperm"
                delete_query = "DELETE FROM searches WHERE search_id = %s"
                cursor.execute(delete_query, (search_id,))
                cls.connection.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error deleting search: {e}")
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def change_search(cls, search_id, search_for, link, properties, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                search_query = "SELECT * FROM searches WHERE search_id = %s"
                cursor.execute(search_query, (search_id,))
                search_data = cursor.fetchone()
                print(search_data[-1],creator_id)
                if search_data[-1] == creator_id:
                    update_query = """
                                        UPDATE searches SET 
                                        search_for = %s, 
                                        link = %s, 
                                        properties = %s,
                                        list_seti = %s
                                        WHERE search_id = %s;"""
                    cursor.execute(update_query, (
                        search_for, link, properties, (False if properties == "" else True), search_id
                    ))
                    cls.connection.commit()
                    return Search(search_id, search_for, link, properties, (False if properties == "" else True),
                                  search_data[5], search_data[6], creator_id).__dict__
                return "0xperm"
        except psycopg2.Error as e:
            print("Error changing search:", e)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
SearchesDB.create_searches_table()
