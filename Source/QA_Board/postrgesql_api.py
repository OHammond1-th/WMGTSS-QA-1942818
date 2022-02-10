import psycopg2 as psql
from psycopg2 import extras as psqx
import sys


class DB_API:

    def __init__(self, dbname, user, password):
        self.database = psql.connect(f"dbname='{dbname}' user='{user}' password='{password}'")
        self.cursor = self.database.cursor()
        self.result_buffer = None

    def set_cursor_tuple(self):
        self.database.commit()
        self.cursor = self.database.cursor()

    def set_cursor_dict(self):
        self.database.commit()
        self.cursor = self.cursor(cursor_factory=psqx.DictCursor)

    def query(self, query):
        try:
            print(query)
            self.cursor.execute(query)

            # psycopg2 throws an error if no results are found but we just want it to set the result buffer to None
            try:
                self.result_buffer = self.cursor.fetchall()
            except Exception as e:
                self.result_buffer = None

        except psql.Error as e:
            print("Query failed:", e.pgerror, e)
            self.database.rollback()

        return self.result_buffer

    def commit(self):
        self.database.commit()

    def rollback(self):
        self.database.rollback()

    def get_result(self, amount=None):
        if self.result_buffer is None:
            return []

        self.database.commit()

        if amount:
            amount = min(amount, len(self.result_buffer))
            return self.result_buffer[:amount]
        return self.result_buffer

    def __str__(self):
        return self.result_buffer

    def __repr__(self):
        return self.result_buffer
