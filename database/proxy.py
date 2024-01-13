import json

import psycopg2

from database import postgres
from database.servers import ServersDB


class Proxy:
    def __init__(self, proxy_id, name, server_id, address, status, creator_id):
        self.proxy_id = proxy_id
        self.server_id = server_id
        self.name = name
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
                    proxy_id SERIAL PRIMARY KEY,
                    server_id INT NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    address TEXT NOT NULL,
                    activity BOOLEAN NOT NULL,
                    creator_id INTEGER NOT NULL
                );
                """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error creating proxy table(proxy.py):", e)
            cursor.close()

    @classmethod
    def add_proxy(cls, server_id, name, address, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                count_query = "SELECT COUNT(*) FROM proxy WHERE server_id = %s"
                cursor.execute(count_query, (server_id,))
                count = cursor.fetchone()[0]
                if count >= 3:
                    return "0xc"

                insert_query = (
                    "INSERT INTO proxy (server_id, name, address, activity, creator_id) "
                    "VALUES (%s, %s, %s, %s, %s) RETURNING proxy_id"
                )
                cursor.execute(insert_query, (server_id, name, address, True, creator_id))
                proxy_id = cursor.fetchone()[0]
                ServersDB.change_proxy_flag(server_id, True, creator_id)
                cls.connection.commit()
                return proxy_id
        except psycopg2.Error as e:
            print("Error adding proxy(proxy.py):", e)
            cls.connection.rollback()
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def delete_proxy(cls, proxy_id,creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT creator_id FROM proxy where proxy_id = %s"
                cursor.execute(select_query, (proxy_id,))
                creator_id_from_db = cursor.fetchone()[0]
                if creator_id_from_db != creator_id:
                    return "0xperm"
                delete_query = "DELETE FROM proxy WHERE proxy_id = %s RETURNING server_id"
                cursor.execute(delete_query, (proxy_id,))
                server_id = cursor.fetchone()[0]

                check_query = "SELECT * FROM proxy WHERE server_id = %s"
                cursor.execute(check_query, (server_id,))

                if not len(cursor.fetchall()):
                    ServersDB.change_proxy_flag(server_id, False,creator_id)
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
    def get_proxy_by_server_id(cls, server_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE server_id = %s"
                cursor.execute(select_query, (server_id,))
                proxy_data = cursor.fetchone()
                return Proxy(*proxy_data).__dict__ if proxy_data else None
        except psycopg2.Error as e:
            print("Error getting proxy by ID(proxy.py):", e)
            cls.connection.rollback()
            return None
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

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
            cls.connection.rollback()
            return None
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

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
            cls.connection.rollback()
            print("Error showing proxies:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def change_proxy(cls, proxy_id, name, address,creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT creator_id FROM proxy WHERE proxy_id = %s"
                cursor.execute(select_query, (proxy_id,))
                fetch = cursor.fetchone()
                if fetch is None:
                    return "0xdb"
                creator_id_from_db = fetch[0]

                if creator_id_from_db != creator_id:
                    return "0xperm"
                update_query = "UPDATE proxy SET name = %s, address = %s WHERE proxy_id = %s RETURNING server_id,activity,creator_id"
                cursor.execute(update_query, (name, address, proxy_id,))
                proxy_data = cursor.fetchone()
                return Proxy(proxy_id, proxy_data[0], name,address, proxy_data[1], proxy_data[2]).__dict__
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error changing proxy:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def change_proxy_activity(cls, proxy_id,creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM proxy WHERE proxy_id = %s"
                cursor.execute(select_query, (proxy_id,))
                fetch_data = cursor.fetchone()
                if fetch_data is None:
                    return "0xdb"
                user_data = fetch_data
                if user_data[-1] == creator_id:
                    update_query = "UPDATE proxy SET activity = %s WHERE proxy_id = %s"
                    cursor.execute(update_query, (not user_data[3], proxy_id,))
                    cls.connection.commit()
                    cursor.close()
                    return not user_data[3]
                return "0xperm"
        except psycopg2.Error as e:
            cls.connection.rollback()
            cursor.close()
            print("Error changing user activity:", e)
            return "0xdb"
        except TypeError as te:
            print("Wrong data! ",te)
            cls.connection.rollback()
            return "0xdb"

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования/
ProxyDB.create_proxy_table()
