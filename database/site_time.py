import time
from datetime import datetime
import json

from database import postgres
from scripts.date import get_month_name

class SiteTime:
    def __init__(self, time_id, emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min,number_of_transitions_max,
                 creator_id):
        self.time_id = time_id
        self.emulation_of_inactivity_min = emulation_of_inactivity_min
        self.emulation_of_inactivity_max = emulation_of_inactivity_max
        self.make_transitions = make_transitions
        self.emulation_of_inactivity_between_articles_min = emulation_of_inactivity_between_articles_min
        self.emulation_of_inactivity_between_articles_max = emulation_of_inactivity_between_articles_max
        self.number_of_transitions_min = number_of_transitions_min
        self.number_of_transitions_max = number_of_transitions_max
        self.creator_id = creator_id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class SiteTimeDB:
    connection = postgres.conn

    @classmethod
    def create_link_table(cls):
        cursor = cls.connection.cursor()
        create_table_query = """
            CREATE TABLE IF NOT EXISTS links (
                link_id SERIAL PRIMARY KEY,
                link TEXT NOT NULL,
                leads_to_post BOOLEAN NOT NULL,
                to_a_specific_link BOOLEAN NOT NULL,
                spec_links TEXT NOT NULL,
                time VARCHAR(255) NOT NULL,
                traffic INTEGER NOT NULL,
                activity BOOLEAN NOT NULL,
                created_at BIGINT NOT NULL,
                creator_id INTEGER NOT NULL
            );
            """
        cursor.execute(create_table_query)
        cls.connection.commit()
        cursor.close()

    @classmethod
    def add_link(cls, link, leads_to_post, spec_links, link_time, traffic, creator_id):
        cursor = cls.connection.cursor()
        insert_query = (
            "INSERT INTO links (link, leads_to_post, to_a_specific_link, spec_links, time, traffic, activity, created_at,creator_id) "
            "VALUES (%s, %s, %s, %s,%s, %s,%s, %s, %s) RETURNING link_id")
        cursor.execute(insert_query, (link, leads_to_post, (False if spec_links == "" else True),
                                          spec_links, link_time, traffic, True, time.time(), creator_id,))
        link_id = cursor.fetchone()[0]
        cls.connection.commit()
        cursor.close()
        return link_id

    @classmethod
    def show_links(cls, creator_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM links WHERE creator_id = %s"
        cursor.execute(select_query, (creator_id,))
        links_data = cursor.fetchall()
        links = []
        for link_data in links_data:
            links.append(Link(*link_data).__dict__)
        cursor.close()
        return links

    @classmethod
    def change_link_activity(cls, link_id):
        cursor = cls.connection.cursor()
        select_query = "SELECT * FROM links WHERE link_id = %s"
        cursor.execute(select_query, (link_id,))
        link_data = cursor.fetchone()
        update_query = "UPDATE links SET activity = %s WHERE link_id = %s"
        cursor.execute(update_query, (not (link_data[6]), (link_id,)))
        cls.connection.commit()
        cursor.close()
        return not (link_data[6])

    @classmethod
    def close_connection(cls):
        cls.connection.close()

# Пример использования
SiteTime.create_user_table()