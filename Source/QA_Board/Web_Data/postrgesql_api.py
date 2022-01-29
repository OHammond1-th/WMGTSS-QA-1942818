import psycopg2 as psql
import psycopg2.extras as psqx


class DB_API:

    def __init__(self, dbname, user, password):
        self.database = psql.connect(f"dbname='{dbname}' user='{user}' password='{password}'")
        self.result_buffer = []

    def query(self, query, cursor=None):
        cursor = self.database.cursor(cursor_factory=psqx.DictCursor) if None else cursor
        self.result_buffer.append(cursor.execute(query).fetchall())

    def transaction(self, querys, cursor=None):
        for query in querys:
            self.query(query, cursor)

    def get_result(self, index=0):
        return self.result_buffer[index]

    def flush_results(self):
        self.result_buffer = []

    def __str__(self):
        return self.result_buffer

    def __repr__(self):
        return self.result_buffer
