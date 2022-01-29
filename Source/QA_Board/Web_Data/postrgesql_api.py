import psycopg2 as psql
import psycopg2.extras as psqx


class DB_API:

    def __init__(self):
        self.database = psql.connect("dbname='WMGTSS_QA' user='web_client' password='default'")
        self.result_buffer = []

    def select(self, query, cursor=None):
        cursor = self.database.cursor(cursor_factory=psqx.DictCursor) if None else cursor
        self.result_buffer.append(cursor.execute(query).fetchall())
