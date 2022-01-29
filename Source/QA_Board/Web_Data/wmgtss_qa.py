import psycopg2 as psql
from .postrgesql_api import DB_API

database = DB_API("WMGTSS_QA", "web_client", "default")


def get_table(table, columns="*", constraints=""):
    try:
        database.query(f"SELECT {columns} FROM {table} {constraints}")
        return database.get_result()
    except psql.Error:
        return None


def get_user(user_id):
    return get_table('users', '*', f"WHERE 'users'('user_id') = {user_id}")


def get_published_posts():
    return get_table('posts', '*', f"WHERE 'posts'('post_published') = TRUE")


def get_posts_by_user(user_id):
    return get_table('posts', '*', f"WHERE 'posts'('author_id') = {user_id}")