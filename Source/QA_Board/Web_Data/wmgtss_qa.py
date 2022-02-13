import datetime

import psycopg2 as psql
from postrgesql_api import DB_API


def to_list(val):
    if type(val) is not list:
        val = [val]
    return val


class DB_singleton(DB_API):

    def __init__(self, dbname, user, password):
        super().__init__(dbname, user, password)

    def select_from_table(self, table, columns="*", constraints=""):
        try:
            self.query(f"SELECT {columns} FROM {table} {constraints}")

            if len(self.get_result()) > 1:
                return self.get_result()
            elif len(self.get_result()) > 0:
                return self.get_result()[0]
            else:
                return []
        except psql.Error:
            return None

    def insert_into_table(self, table, columns, values):
        try:
            print(values)
            return self.query(f"INSERT INTO {table}({columns}) VALUES ({values}) RETURNING {table[:-1]}_id")
        except psql.Error:
            return None

    def update_table_row(self, table, columns: list, values: list, primary_key):
        if len(columns) != len(values):
            return False

        # Create the list of columns and changes we would like to make
        col_vals = ""

        for column, value in zip(columns, values):
            # if the input will be of type date or string then put quote marks around it
            if type(value) is datetime.datetime or type(value) is str:
                value = f"'{value}'"

            col_vals += f"{column} = {value}"

        try:
            self.query(f"UPDATE {table} SET {col_vals} WHERE {table[:-1]}_id = {primary_key}")
            return True
        except psql.Error:
            return False

    def delete_from_table(self, table, _id):
        try:
            self.query(f"DELETE FROM {table} WHERE {table}.{table[:-1]}_id = {_id}")
            return True
        except psql.Error:
            return False

    def get_course_by_id(self, course_id):
        return self.select_from_table('courses', '*', f"WHERE courses.course_id = '{course_id}'")

    def get_user(self, user_id):
        return self.select_from_table('users', '*', f"WHERE users.user_id = '{user_id}'")

    def get_user_by_username(self, username):
        return self.select_from_table('users', '*', f"WHERE users.user_username = '{username}'")

    def get_users_by_role(self, role):
        result =  self.select_from_table('users', '*', f"FULL OUTER JOIN roles ON roles.role_id = users.role_id"
                                               f" WHERE roles.role_name = '{role.lower()}'")
        return to_list(result)

    def get_users_enrollments(self, user_id):
        result = self.select_from_table('enrollments', 'course_id', f"WHERE enrollments.user_id = '{user_id}'")
        return to_list(result)

    def get_user_elevation(self, user_id):
        return self.select_from_table('users', 'roles.role_elevated', f"FULL OUTER JOIN roles "
                                                                      f"ON roles.role_id = users.role_id"
                                                                      f" WHERE users.user_id = {user_id}")

    def get_posts_by_class(self, class_id):
        result = self.select_from_table('posts', '*', f"WHERE posts.course_id = '{class_id}'")
        return to_list(result)

    def get_posts_by_user(self, user_id):
        result = self.select_from_table('posts', '*', f"WHERE posts.author_id = '{user_id}'")
        return to_list(result)

    def get_post_comments(self, post_id):
        result = self.select_from_table('comments', '*', f"WHERE comments.post_id = '{post_id}'")
        return to_list(result)

    def get_post(self, post_id):
        return self.select_from_table('posts', '*', f"WHERE posts.post_id = '{post_id}'")

    def insert_into_posts(self, course_id, author_id, title, description, publishable):
        return self.insert_into_table('posts', 'course_id, author_id, post_title, post_description, post_publishable',
                                      f"{course_id}, {author_id}, '{title}', '{description}', {publishable}")

    def insert_into_comments(self, post_id, author_id, description, parent_id=None):
        return self.insert_into_table('comments', 'post_id, author_id, parent_id, comment_description',
                                      f"{post_id}, {author_id}, {parent_id}, '{description}'")

    def set_user_password(self, user_id, password):
        return self.update_table_row('users', ['user_password'], [password], user_id)

    def update_question_with_answer(self, question_id, answer):
        return self.update_table_row('posts', ['post_answer'], [answer], question_id)

    def delete_from_questions(self, question_id):
        return self.delete_from_table('posts', question_id)


db = DB_singleton("WMGTSS_QA", "web_client", "default")
