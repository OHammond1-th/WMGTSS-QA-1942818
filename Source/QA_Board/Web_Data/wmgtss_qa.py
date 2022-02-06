import psycopg2 as psql
from postrgesql_api import DB_API

database = DB_API("WMGTSS_QA", "web_client", "default")


def select_from_table(table, columns="*", constraints=""):
    try:
        database.query(f"SELECT {columns} FROM {table} {constraints}")
        return database.get_result()
    except psql.Error:
        return None


def insert_into_table(table, columns, values):
    try:
        return database.query(f"INSERT INTO {table}({columns}) VALUES ({values}) RETURNING {table[:-1]}_id")
    except psql.Error:
        return None


def update_table_row(table, columns: list, values: list, primary_key):
    if len(columns) != len(values):
        return False

    col_vals = "".join([f"{column} = {value},\n" for column, value in zip(columns, values)])

    try:
        database.query(f"UPDATE {table} SET {col_vals} WHERE {table[:-1]}_id = {primary_key}")
        return True
    except psql.Error:
        return False


def get_course_by_id(course_id):
    return select_from_table('courses', '*', f"WHERE courses.course_id = '{course_id}'")


def get_user(user_id):
    return select_from_table('users', '*', f"WHERE users.user_id = '{user_id}'")


def get_user_by_username(username):
    return select_from_table('users', '*', f"WHERE users.user_username = '{username}'")


def get_users_by_role(role):
    return select_from_table('users', '*', f"OUTER JOIN roles AT roles.role_id = users.role_id"
                             f" WHERE roles.role_name = '{role.lower()}'")


def get_published_posts():
    return select_from_table('posts', '*', f"WHERE posts.post_published = TRUE")


def get_posts_by_class(class_id):
    return select_from_table('posts', '*', f"WHERE posts.course_id = '{class_id}'")


def get_posts_by_user(user_id):
    return select_from_table('posts', '*', f"WHERE posts.author_id = '{user_id}'")


def get_post_comments(post_id):
    return select_from_table('comments', '*', f"WHERE comments.parent_id = '{post_id}'")


def get_post(post_id):
    return select_from_table('posts', '*', f"WHERE posts.post_id = '{post_id}'")


def get_users_enrollments(user_id):
    return select_from_table('enrollments', 'course_id', f"WHERE enrollments.user_id = '{user_id}'")


def insert_into_posts(course_id, author_id, title, description, publishable):
    return insert_into_table('posts', 'course_id, author_id, post_title, post_description, post_publishable',
                             f'{course_id}, {author_id}, {title}, {description}, {publishable}')


def insert_into_comments(post_id, author_id, description, parent_id=None):
    return insert_into_table('comments', 'post_id, author_id, parent_id, comment_description',
                             f'{post_id}, {author_id}, {parent_id}, {description}')
