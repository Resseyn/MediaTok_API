import json

from database import postgres
from database.postgres import SingletonMeta


class Client:
    def __init__(self, client_id, login, password):
        self.client_id = client_id
        self.login = login
        self.password = password
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

class ClientsDB(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = postgres.conn
        self.cursor = self.connection.cursor()

    def create_client_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS clients (
            client_id SERIAL PRIMARY KEY,
            login VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL
        );
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def add_client(self, login, password):
        insert_query = ("INSERT INTO clients (login, password) "
                        "VALUES (%s, %s) RETURNING user_id")
        self.cursor.execute(insert_query, (login, password))
        user_id = self.cursor.fetchone()[0]
        self.connection.commit()
        return user_id

    def get_user_by_auth(self, login, password):
        select_query = "SELECT * FROM clients WHERE login = %s AND password = %s"
        self.cursor.execute(select_query, (login, password))
        user_data = self.cursor.fetchone()
        if user_data is None:
            return None
        user = Client(*user_data)
        return user


    def close_connection(self):
        self.cursor.close()
        self.connection.close()

# Пример использования
clients_db = ClientsDB()
clients_db.create_client_table()
