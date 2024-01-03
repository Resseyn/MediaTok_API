import json

from database import postgres


class Link:
    def __init__(self, link_id, link, spec_links, time, traffic,  activity, created_at, creator_id):
        self.link_id = link_id
        self.link = link
        self.spec_links = spec_links
        self.time = time
        self.traffic = traffic
        self.activity =  activity
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
            spec_links TEXT [] NOT NULL,
            time VARCHAR(255) NOT NULL,
            traffic INTEGER NOT NULL,
            activity BOOLEAN NOT NULL,
            created_at BIGINT NOT NULL,
            creator_id INTEGER NOT NULL,
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_link(cls, login, password):
        insert_query = ("INSERT INTO links (link, spec_links, time, traffic, created_at, creator_id) "
                        "VALUES (%s, %s) RETURNING user_id")
        cls.cursor.execute(insert_query, (login, password))
        user_id = cls.cursor.fetchone()[0]
        cls.connection.commit()
        return user_id

    @classmethod
    def show_links(cls, client_id):
        select_query = "SELECT * FROM links WHERE creator_id = %s"
        cls.cursor.execute(select_query, (client_id,))
        users_data = cls.cursor.fetchall()
        users = []
        for user_data in users_data:
            users.append(Link(*user_data).__dict__)
        return users


    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()

# Пример использования
LinksDB.create_link_table()
