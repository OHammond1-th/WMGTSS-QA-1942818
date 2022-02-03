import psycopg2 as psql
import psycopg2.extras as psqx


class DB_API:

    def __init__(self, dbname, user, password):
        self.database = psql.connect(f"dbname='{dbname}' user='{user}' password='{password}'")
        self.cursor = self.database.cursor(cursor_factory=psqx.DictCursor)
        self.result_buffer = None

    def query(self, query):
        try:
            self.result_buffer = self.cursor.execute(query).fetchall()
        except psql.Error:
            print("Query failed")
            self.cursor.rollback()

    def commit(self):
        self.cursor.commit()

    def rollback(self):
        self.cursor.rollback()

    def get_result(self):
        self.cursor.commit()
        return self.result_buffer

    def __str__(self):
        return self.result_buffer

    def __repr__(self):
        return self.result_buffer
