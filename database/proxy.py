import json
import psycopg2
from database import postgres
from database.servers import ServersDB


class Proxy:
    def __init__(self, proxy_id, server_id, address, status, creator_id):
        self.proxy_id = proxy_id
        self.server_id = server_id
        self.address = address
        self.status = status
        self.creator_id = creator_id

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

class ProxyDB:
    connection = postgres.conn

    @classmethod
    def create_proxy_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS proxy (
                    proxy_id INT PRIMARY KEY,
                    server_id INT NOT NULL,
                    address TEXT NOT NULL,
                    status BOOLEAN NOT NULL,
                    creator_id INTEGER NOT NULL
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            print("Error creating proxy table(proxy.py):", e)

    @classmethod
    def add_proxy(cls, server_id, address, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                count_query = "SELECT COUNT(*) FROM proxy WHERE server_id = %s"
                cursor.execute(count_query, (server_id,))
                count = cursor.fetchone()[0]

                if count > 3:
                    print("Too many proxies for this server_id")
                    return None

                insert_query = (
                    "INSERT INTO proxy (server_id, address, status, creator_id) "
                    "VALUES (%s, %s, %s, %s) RETURNING proxy_id"
                )
                cursor.execute(insert_query, (server_id, address, True, creator_id))
                proxy_id = cursor.fetchone()[0]
                cls.connection.commit()
                return proxy_id
        except psycopg2.Error as e:
            print("Error adding proxy(proxy.py):", e)
            return None

    @classmethod
    def delete_proxy(cls, proxy_id):
        try:
            with cls.connection.cursor() as cursor:
                delete_query = ("DELETE FROM proxy WHERE proxy_id = %s RETURNING server_id")
                cursor.execute(delete_query, (proxy_id,))
                server_id = cursor.fetchone()[0]

                check_query = ("SELECT * FROM proxy WHERE server_id = %s")
                cursor.execute(check_query, (server_id,))

                if len(cursor.fetchall()):
                    ServersDB.change_proxy_flag(server_id, False)
                return True
        except psycopg2.Error as e:
            print("Error deleting proxy:", e)
            return False

    @classmethod
    def get_proxy_by_server_id(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                proxy_data = cursor.fetchone()
                return Proxy(*proxy_data).__dict__ if proxy_data else None
        except psycopg2.Error as e:
            print("Error getting proxy by ID(proxy.py):", e)
            return None

    @classmethod
    def get_proxy_by_proxy_id(cls, proxy_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE proxy_id = %s"
                cursor.execute(select_query, (proxy_id,))
                proxy_data = cursor.fetchone()
                return Proxy(*proxy_data).__dict__ if proxy_data else None
        except psycopg2.Error as e:
            print("Error getting proxy by ID(proxy.py):", e)
            return None

    @classmethod
    def show_proxies(cls, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                proxies_data = cursor.fetchall()
                proxies = [Proxy(*proxy_data).__dict__ for proxy_data in proxies_data]
                return proxies
        except psycopg2.Error as e:
            print("Error showing proxies:", e)
            return []

    def change_proxy(cls, proxy_id, address, status):
        try:
            with cls.connection.cursor() as cursor:
                update_query = "UPDATE proxy SET address = %s, status = %s WHERE proxy_id = %s RETURNING server_id,creator_id"
                cursor.execute(update_query, (address, status, proxy_id))
                proxy_data = cursor.fetchone()
                return Proxy(proxy_id, proxy_data[0], address, status, proxy_data[1]).__dict__
        except psycopg2.Error as e:
            print("Error changing proxy:", e)
            return None


    @classmethod
    def close_connection(cls):
        cls.connection.close()

# Пример использования
ProxyDB.create_proxy_table()