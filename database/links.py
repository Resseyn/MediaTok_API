import json
import time

from database import postgres

class Link:
    def __init__(self, link_id, link, leads_to_post, to_a_specific_link, spec_links, time, traffic,  activity, created_at, creator_id):
        self.link_id = link_id
        self.link = link
        self.leads_to_post = leads_to_post
        self.to_a_specific_link = to_a_specific_link
        self.spec_links = spec_links
        self.time = time
        self.traffic = traffic
        self.activity = activity
        self.created_at = created_at
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class LinksDB():
    connection = postgres.conn
    cursor = connection.cursor()

    @classmethod
    def create_link_table(cls):
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
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_link(cls, link, leads_to_post, spec_links, link_time, traffic, creator_id):
        insert_query = ("INSERT INTO links (link, leads_to_post, to_a_specific_link, spec_links, time, traffic, activity, created_at,creator_id) "
                        "VALUES (%s, %s, %s, %s,%s, %s,%s, %s, %s) RETURNING link_id")
        cls.cursor.execute(insert_query, (link, leads_to_post, (False if spec_links == "" else True),
                                          spec_links, link_time, traffic, True, time.time(), creator_id,))
        link_id = cls.cursor.fetchone()[0]
        cls.connection.commit()
        return link_id

    @classmethod
    def show_links(cls, creator_id):
        select_query = "SELECT * FROM links WHERE creator_id = %s"
        cls.cursor.execute(select_query, (creator_id,))
        links_data = cls.cursor.fetchall()
        links = []
        for link_data in links_data:

            links.append(Link(*link_data).__dict__)
        return links

    @classmethod
    def change_link_activity(cls, link_id):
        select_query = "SELECT * FROM links WHERE link_id = %s"
        cls.cursor.execute(select_query, (link_id,))
        link_data = cls.cursor.fetchone()
        update_query = "UPDATE links SET activity = %s WHERE link_id = %s"
        cls.cursor.execute(update_query, (not (link_data[6]), (link_id,)))
        cls.connection.commit()
        return not (link_data[6])
    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()

# Пример использования
LinksDB.create_link_table()
