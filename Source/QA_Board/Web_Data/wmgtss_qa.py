# Builtin imports
import datetime

# Local and External imports
import psycopg2 as psql
from postrgesql_api import DB_API


def to_list(val):
    """
    Helper function to convert non list values to a list
    :param val: Value to convert
    :return:
    """
    if type(val) is not list:
        val = [val]
    return val


class DB_singleton(DB_API):

    """
    Database API that inherits from DB_API to provide bespoke custom queries that can be used by the models
    to request updates or provide new information to the database.
    """

    def __init__(self, dbname, user, password):
        super().__init__(dbname, user, password)

    def set_db(self, database):
        """
        Function to replace the database connection when required - for example changing to a test database
        :param database: The database connection to change to
        :return:
        """
        self.database.close()
        self.database = database

    def select_one_random(self, table):
        """
        Selects a random row from the table provided
        :param table: The table from which a row will be selected
        :return:
        """
        try:
            self.query(f"SELECT * FROM {table} ORDER BY random() LIMIT 1")
            return self.get_result()
        except psql.Error:
            return None

    def select_from_table(self, table, columns="*", constraints=""):
        """
        Constructs a select query from the provided arguments
        :param table: The table from which to query
        :param columns: The columns to return
        :param constraints: Any joins or constraints that will affect the data returned
        :return: The selected values
        """
        try:
            self.query(f"SELECT {columns} FROM {table} {constraints}")

            # If there is more than one value return it immediately otherwise return the first item
            # this is necessary because when a fetch is made using tuple cursor a single value will
            # still be encapsulated by the tuple
            if len(self.get_result()) > 1:
                return self.get_result()
            elif len(self.get_result()) > 0:
                return self.get_result()[0]
            else:
                return []
        except psql.Error:
            return None

    def insert_into_table(self, table, columns, values):
        """
        Constructs an insert query from the provided arguments
        :param table: The table from which to query
        :param columns: The columns to provide values for
        :param values: The values to insert
        :return: The id of the inserted value
        """
        try:
            print(values)
            return self.query(f"INSERT INTO {table}({columns}) VALUES ({values}) RETURNING {table[:-1]}_id")
        except psql.Error:
            return None

    def update_table_row(self, table, columns: list, values: list, primary_key):
        """
        Constructs an update query from the provided arguments
        :param table: The table from which to query
        :param columns: The columns to provide values for
        :param values: The values to update
        :param primary_key: The id of the row to update
        :return: Whether the query was successful
        """
        if len(columns) != len(values):
            return False

        # Create the list of columns and changes we would like to make
        col_vals = ""

        for column, value in zip(columns, values):
            # if the input will be of type date or string then put quote marks around it
            if type(value) is datetime.datetime or type(value) is str:
                value = f"'{value}'"

            # Construct string pairs of columns and values that are concatenated
            col_vals += f"{column} = {value}"

        try:
            self.query(f"UPDATE {table} SET {col_vals} WHERE {table[:-1]}_id = {primary_key}")
            return True
        except psql.Error:
            return False

    def delete_from_table(self, table, _id):
        """
        Constructs a delete query with the provided arguments
        :param table: The tables to delete from
        :param _id: The id of the row to delete
        :return: Whether the query was successful
        """
        try:
            self.query(f"DELETE FROM {table} WHERE {table}.{table[:-1]}_id = {_id}")
            return True
        except psql.Error:
            return False

    def get_course_by_id(self, course_id):
        """
        Return course by id
        :param course_id: The id of the course requested
        :return: The row of courses requested
        """
        return self.select_from_table('courses', '*', f"WHERE courses.course_id = '{course_id}'")

    def get_course_by_name(self, course_name):
        """
        Return course by name
        :param course_name: The name of the course requested
        :return: The row of courses requested
        """
        return self.select_from_table('courses', '*', f"WHERE courses.course_name = '{course_name}'")

    def get_user(self, user_id):
        """
        Return a user by their id
        :param user_id: The id of the user
        :return: The users row to return
        """
        return self.select_from_table('users', '*', f"WHERE users.user_id = '{user_id}'")

    def get_user_by_username(self, username):
        """
        Return a user by their username
        :param username: The username of the user
        :return: The users row to return
        """
        return self.select_from_table('users', '*', f"WHERE users.user_username = '{username}'")

    def get_users_by_role(self, role):
        """
        Get all the users that are under the given role
        :param role: The role that has been requested
        :return: All users of the given role
        """
        result =  self.select_from_table('users', '*', f"FULL OUTER JOIN roles ON roles.role_id = users.role_id"
                                               f" WHERE roles.role_name = '{role.lower()}'")
        return to_list(result)

    def get_users_enrollments(self, user_id):
        """
        Get all the courses a user is enrolled in
        :param user_id: The users id
        :return: The courses they have enrolled in
        """
        result = self.select_from_table('enrollments', 'course_id', f"WHERE enrollments.user_id = '{user_id}'")
        return to_list(result)

    def get_user_elevation(self, user_id):
        """
        Return if a user is considered elevated
        :param user_id: The users id
        :return: True if the user is elevated
        """
        return self.select_from_table('users', 'roles.role_elevated', f"FULL OUTER JOIN roles "
                                                                      f"ON roles.role_id = users.role_id"
                                                                      f" WHERE users.user_id = {user_id}")

    def get_posts_by_class(self, class_id):
        """
        Get all the posts associated with the given class
        :param class_id: The classes id
        :return: All posts associated
        """
        result = self.select_from_table('posts', '*', f"WHERE posts.course_id = '{class_id}'")
        return to_list(result)

    def get_posts_by_user(self, user_id):
        """
        Get all posts associated with the given user
        :param user_id: The users id
        :return: All posts associated
        """
        result = self.select_from_table('posts', '*', f"WHERE posts.author_id = '{user_id}'")
        return to_list(result)

    def get_post_comments(self, post_id):
        """
        Get all the comments associated with the given post in newest first order
        :param post_id: The post id
        :return: All comments associated
        """
        result = self.select_from_table('comments', '*', f"WHERE"
                                                         f" comments.post_id = '{post_id}' "
                                                         f"ORDER BY"
                                                         f" comments.comment_created DESC")
        return to_list(result)

    def get_post(self, post_id):
        """
        Get a post by its id
        :param post_id: The posts id
        :return: The posts row to return
        """
        return self.select_from_table('posts', '*', f"WHERE posts.post_id = '{post_id}'")

    def insert_into_posts(self, course_id, author_id, title, description, publishable):
        """
        Creates a new post row and inserts it
        :param course_id: The courses id
        :param author_id: The authors id
        :param title: The given title of the post
        :param description: The given description of the post
        :param publishable: Whether the post is able to be published
        :return: The id of the new post
        """
        return self.insert_into_table('posts', 'course_id, author_id, post_title, post_description, post_publishable',
                                      f"{course_id}, {author_id}, '{title}', '{description}', {publishable}")

    def insert_into_comments(self, post_id, author_id, description, parent_id=None):
        """
        Creates a new comment row and inserts it
        :param post_id: The posts id
        :param author_id: The author users id
        :param description: The given description
        :param parent_id: The parent comment if one is given
        :return: The id of the new comment
        """
        return self.insert_into_table('comments', 'post_id, author_id, parent_id, comment_description',
                                      f"{post_id}, {author_id}, {parent_id}, '{description}'")

    def set_user_password(self, user_id, password):
        """
        Sets the user a new password that should be hashed beforehand
        :param user_id: The users id
        :param password: The new password to provide
        :return: Success status
        """
        return self.update_table_row('users', ['user_password'], [password], user_id)

    def set_publish_state(self, post_id, state: bool):
        """
        Sets the given posts state of published
        :param post_id: The posts id
        :param state: Whether the post is published
        :return: Success state
        """
        return self.update_table_row('posts', ['post_published'], [state], post_id)

    def update_post_with_answer(self, post_id, answer):
        """
        Updates the answer field of a post
        :param post_id: The posts id
        :param answer: The current answer to update with
        :return: Success state
        """
        return self.update_table_row('posts', ['post_answer'], [answer], post_id)

    def delete_from_posts(self, post_id):
        """
        Deletes a given post by its id
        :param post_id: The posts id
        :return: Success state
        """
        return self.delete_from_table('posts', post_id)

    def delete_comment(self, comment_id):
        """
        Deletes a given comment by its id
        :param comment_id: The comments id
        :return: Success state
        """
        return self.update_table_row('comments', ['comment_description'], ['<comment deleted>'], comment_id)

    def get_random_course(self):
        """
        Gets a random course row
        :return: The course row to return
        """
        return self.select_one_random("courses")

    def get_random_user(self):
        """
        Gets a random user row
        :return: The user row to return
        """
        return self.select_one_random("users")
