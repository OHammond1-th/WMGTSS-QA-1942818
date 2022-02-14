import psycopg2 as psql
from psycopg2 import extras as psqx
import sys


class DB_API:

    """
    Database API class that handles queries to and from a database
    """

    def __init__(self, dbname, user, password):
        self.database = psql.connect(f"dbname='{dbname}' user='{user}' password='{password}'")
        self.cursor = self.database.cursor()
        self.result_buffer = None

    def set_cursor_tuple(self):
        """
        Sets the cursor to provide a tuple when asked to fetch results
        :return:
        """
        self.database.commit()
        self.cursor = self.database.cursor()

    def set_cursor_dict(self):
        """
        Sets the cursor to provide a dictionary when asked to fetch results
        :return:
        """
        # If cursor is changing make sure to commit any previous changes first
        self.database.commit()
        self.cursor = self.cursor(cursor_factory=psqx.DictCursor)

    def query(self, query):
        """
        Takes a postgreSQL query and executes it whilst handling any errors that might be returned
        :param query: The query to be executed
        :return:
        """
        try:
            print(query)
            self.cursor.execute(query)

            # psycopg2 throws an error if no results are found but we just want it to set the result buffer to None in
            # that case
            try:
                self.result_buffer = self.cursor.fetchall()
            except Exception as e:
                self.result_buffer = None

        except psql.Error as e:
            # Only catch errors here that are associated to the database itself
            print("Query failed:", e.pgerror, e)
            self.database.rollback()

        return self.result_buffer

    def commit(self):
        """
        Gives any file that creates an instance the ability to commit manually
        :return:
        """
        self.database.commit()

    def rollback(self):
        """
        Gives any file that creates an instance the ability to rollback manually
        :return:
        """
        self.database.rollback()

    def get_result(self, amount=None):
        """
        Returns the results from the previous query
        :param amount: If specified will return that many results limited to the total results available
        :return:
        """
        if self.result_buffer is None:
            return []

        self.database.commit()

        if amount:
            # Only use the amount value given if it is less than the size of the result buffer
            amount = min(amount, len(self.result_buffer))
            # Return only those results requested
            return self.result_buffer[:amount]
        return self.result_buffer

    def __str__(self):
        """
        Function to provide print-ability when debugging
        :return:
        """
        return self.result_buffer

    def __repr__(self):
        """
        Function to provide print-ability when debugging
        :return:
        """
        return self.result_buffer
