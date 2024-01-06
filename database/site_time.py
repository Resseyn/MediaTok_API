import json

import psycopg2

from database import postgres


class SiteTime:
    def __init__(self, emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min, number_of_transitions_max,
                 creator_id):
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
    def create_site_time_table(cls):
        try:
            with cls.connection.cursor() as cursor:
                create_table_query = """
                CREATE TABLE IF NOT EXISTS site_times (
                    emulation_of_inactivity_min INTEGER NOT NULL,
                    emulation_of_inactivity_max INTEGER NOT NULL,
                    make_transitions BOOLEAN NOT NULL,
                    emulation_of_inactivity_between_articles_min INTEGER NOT NULL,
                    emulation_of_inactivity_between_articles_max INTEGER NOT NULL,
                    number_of_transitions_min INTEGER NOT NULL,
                    number_of_transitions_max INTEGER NOT NULL,
                    creator_id INTEGER NOT NULL
                );
            """
                cursor.execute(create_table_query)
                cls.connection.commit()
        except psycopg2.Error as e:
            cls.connection.rollback()
            print(f"Error creating site_times table: {e}")

    @classmethod
    def add_time(cls, emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min, number_of_transitions_max,
                 creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM site_times WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                time_data = cursor.fetchone()
                if time_data is not None:
                    SiteTimeDB.change_times(creator_id,emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min, number_of_transitions_max)
                    return SiteTime(emulation_of_inactivity_min,emulation_of_inactivity_max, make_transitions,
                                emulation_of_inactivity_between_articles_min,emulation_of_inactivity_between_articles_max,
                                number_of_transitions_min, number_of_transitions_max,creator_id).__dict__
                insert_query = (
                    "INSERT INTO site_times (emulation_of_inactivity_min, emulation_of_inactivity_max, "
                    "make_transitions, emulation_of_inactivity_between_articles_min, "
                    "emulation_of_inactivity_between_articles_max, number_of_transitions_min, "
                    "number_of_transitions_max, creator_id) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                )
                cursor.execute(insert_query, (
                    emulation_of_inactivity_min, emulation_of_inactivity_max, make_transitions,
                    emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                    number_of_transitions_min, number_of_transitions_max, creator_id)
                               )
                cls.connection.commit()
                return SiteTime(emulation_of_inactivity_min,emulation_of_inactivity_max, make_transitions,
                                emulation_of_inactivity_between_articles_min,emulation_of_inactivity_between_articles_max,
                                number_of_transitions_min, number_of_transitions_max,creator_id).__dict__
        except psycopg2.Error as e:
            print(f"Error adding time: {e}")
            return None

    @classmethod
    def change_times(cls,creator_id, emulation_of_inactivity_min, emulation_of_inactivity_max,
                 make_transitions,
                 emulation_of_inactivity_between_articles_min, emulation_of_inactivity_between_articles_max,
                 number_of_transitions_min, number_of_transitions_max):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM site_times WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                time_data = cursor.fetchone()
                if time_data:
                    update_query = '''UPDATE site_times 
                SET emulation_of_inactivity_min = %s, 
                    emulation_of_inactivity_max = %s, 
                    make_transitions = %s, 
                    emulation_of_inactivity_between_articles_min = %s,
                    emulation_of_inactivity_between_articles_max = %s,
                    number_of_transitions_min = %s,
                    number_of_transitions_max = %s
                WHERE creator_id = %s'''
                    cursor.execute(update_query, (emulation_of_inactivity_min,emulation_of_inactivity_max,
                                                  make_transitions,emulation_of_inactivity_between_articles_min,
                                                  emulation_of_inactivity_between_articles_max,
                                                  number_of_transitions_min,number_of_transitions_max,creator_id,))
                    cls.connection.commit()
                    return SiteTime(emulation_of_inactivity_min, emulation_of_inactivity_max, make_transitions,
                                    emulation_of_inactivity_between_articles_min,emulation_of_inactivity_between_articles_max,
                                    number_of_transitions_min, number_of_transitions_max,creator_id).__dict__
                return None
        except psycopg2.Error as e:
            cls.connection.rollback()
            print("Error changing site_times:",e)

    @classmethod
    def show_times(cls, creator_id):
        try:
            with cls.connection.cursor() as cursor:
                select_query = "SELECT * FROM site_times WHERE creator_id = %s"
                cursor.execute(select_query, (creator_id,))
                time_data = cursor.fetchone()
                return SiteTime(*time_data).__dict__
        except psycopg2.Error as e:
            cls.connection.rollback()
            print(f"Error showing times: {e}")

    @classmethod
    def close_connection(cls):
        cls.connection.close()


# Пример использования.
SiteTimeDB.create_site_time_table()
