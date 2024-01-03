import json

from database import postgres


class Link:
    def __init__(self, client_id, login, password):
        self.client_id = client_id
        self.login = login
        self.password = password
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class LinksDB():
    connection = postgres.conn
    cursor = connection.cursor()

    @classmethod
    def create_link_table(cls):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        cls.cursor.execute(create_table_query)
        cls.connection.commit()

    @classmethod
    def add_link(cls, login, password):
        insert_query = ("INSERT INTO clients (login, password) "
                        "VALUES (%s, %s) RETURNING user_id")
        cls.cursor.execute(insert_query, (login, password))
        user_id = cls.cursor.fetchone()[0]
        cls.connection.commit()
        return user_id

    @classmethod
    def get_user_by_auth(cls, login, password):
        select_query = "SELECT * FROM clients WHERE login = %s AND password = %s"
        cls.cursor.execute(select_query, (login, password))
        user_data = cls.cursor.fetchone()
        if user_data is None:
            return None
        user = Client(*user_data)
        return user

    @classmethod
    def close_connection(cls):
        cls.cursor.close()
        cls.connection.close()

# Пример использования
ClientsDB.create_client_table()
