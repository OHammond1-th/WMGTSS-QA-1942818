import psycopg2 as psql
from postrgesql_api import DB_API

database = DB_API("WMGTSS_QA", "web_client", "default")


def query_table(table, columns="*", constraints=""):
    try:
        database.query(f"SELECT {columns} FROM {table} {constraints}")
        return database.get_result()
    except psql.Error:
        return None


def get_user(user_id):
    return query_table('users', '*', f"WHERE users.user_id = '{user_id}'")


def get_user_by_username(username):
    return query_table('users', '*', f"WHERE users.user_username = '{username}'")


def get_users_by_role(role):
    return query_table('users', '*', f"OUTER JOIN roles AT roles.role_id = users.role_id"
                                     f" WHERE roles.role_name = '{role.lower()}'")


def get_published_posts():
    return query_table('posts', '*', f"WHERE posts.post_published = TRUE")


def get_posts_by_class(class_id):
    return query_table('posts', '*', f"WHERE posts.course_id = '{class_id}'")


def get_posts_by_user(user_id):
    return query_table('posts', '*', f"WHERE posts.author_id = '{user_id}'")


def get_post_comments(post_id):
    return query_table('comments', '*', f"WHERE comments.parent_id = '{post_id}'")


def get_post(post_id):
    return query_table('posts', '*', f"WHERE posts.post_id = '{post_id}'")


def get_users_enrollments(user_id):
    return query_table('enrollments', 'course_id', f"WHERE enrollments.user_id = '{user_id}'")
