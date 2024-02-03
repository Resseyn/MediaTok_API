import json
import time

import psycopg2

from database import postgres


class Link:
    def __init__(self, link_id, link, leads_to_post, to_a_specific_link, spec_links, traffic, activity,
                 created_at, creator_id):
        self.link_id = link_id
        self.link = link
        self.leads_to_post = leads_to_post
        self.to_a_specific_link = to_a_specific_link
        self.spec_links = spec_links
        self.traffic = traffic
        self.activity = activity
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class LinksDB:
    connection = postgres.conn

    @classmethod
    def create_link_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS links (
                    link_id SERIAL PRIMARY KEY,
                    link TEXT NOT NULL,
                    leads_to_post BOOLEAN NOT NULL,
                    to_a_specific_link BOOLEAN NOT NULL,
                    spec_links TEXT NOT NULL,
                    traffic INTEGER NOT NULL,
                    activity BOOLEAN NOT NULL,
                    created_at BIGINT NOT NULL,
                    creator_id INTEGER NOT NULL
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error creating link table:", e)

    @classmethod
    def add_link(cls, link, leads_to_post, spec_links, traffic, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                insert_query = (
                    "INSERT INTO links (link, leads_to_post, to_a_specific_link, spec_links, traffic, activity, created_at, creator_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *")
                cursor.execute(insert_query, (link, leads_to_post, (False if spec_links == "" else True),
                                              spec_links, traffic, True, time.time(), creator_id,))
                link_id = cursor.fetchone()
                cls.connection.commit()
                return Link(*link_id).__dict__
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error adding link:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def show_links(cls):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM links"
                cursor.execute(select_query,)
                links_data = cursor.fetchall()
                links = [Link(*link_data).__dict__ for link_data in links_data]
                return links
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error showing links:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def change_link_activity(cls, link_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM links WHERE link_id = %s"
                cursor.execute(select_query, (link_id,))
                link_data = cursor.fetchone()
                update_query = "UPDATE links SET activity = %s WHERE link_id = %s"
                cursor.execute(update_query, (not link_data[7], link_id))
                cls.connection.commit()
                return not link_data[7]
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error changing link activity:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def delete_link(cls, link_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT creator_id FROM links WHERE link_id =%s"
                cursor.execute(select_query, (link_id,))
                fetch_data = cursor.fetchone()
                if fetch_data is None:
                    return "0xdb"
                delete_query = "DELETE FROM links WHERE link_id = %s"
                cursor.execute(delete_query, (link_id,))
                cls.connection.commit()
                return True
        except psycopg2.Error as e:
            print("Error deleting proxy:", e)
            cls.connection.rollback()
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def change_link(cls, link_id, link, leads_to_post, spec_links, traffic):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM links WHERE link_id = %s"
                cursor.execute(select_query, (link_id,))
                link_data = cursor.fetchone()
                update_query = '''UPDATE links 
                SET link = %s, 
                    leads_to_post = %s, 
                    to_a_specific_link = %s,
                    spec_links = %s,
                    traffic = %s
                WHERE link_id = %s'''
                cursor.execute(update_query, (
                    link, leads_to_post, (False if spec_links == "" else True), spec_links, traffic,
                    link_id))
                cls.connection.commit()
                return Link(link_id, link, leads_to_post, (False if spec_links == "" else True), spec_links,
                            traffic, link_data[7], link_data[8], link_data[9]).__dict__

        except psycopg2.Error as e:
            print(f"Error changing link:", e)
            cls.connection.rollback()
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
LinksDB.create_link_table()
