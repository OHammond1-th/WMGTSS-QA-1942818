from postrgesql_api import DB_API
from sys import argv
from os.path import exists
import re

database = None


def set_database(new_database):
    """
    Change the current database connection
    :param new_database:
    :return:
    """
    global database
    database = new_database


def create_new_course(name, start, end=None):
    """
    Creates a new course in the database
    :param name: Course name
    :param start: Course start
    :param end: Course end
    :return:
    """

    # if an end is provided convert it to string
    if end:
        end = str(end)

    database.query(
        f"INSERT INTO "
        f"courses(course_name, course_start, course_end) "
        f"VALUES "
        f"('{name}', '{start}', '{end}') "
    )


def query_from_file(file_path):
    """
    Iterate down a csv file and call create_new_course
    :param file_path: The file to iterate over
    :return:
    """
    lines = None

    # read file into memory
    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        # for each line create a new course
        for line in lines:
            line_args = line[:-1].split(',')

            create_new_course(*line_args)

            commit()

    except ValueError as e:
        # print an error if something has gone wrong
        print(f"Args did not meet those required:\t{e}/2-3")
        database.rollback()


def commit():
    # manual database commit
    database.commit()


if __name__ == "__main__":

    database = DB_API("WMGTSS_QA_TEST", "administrator", "default")

    if exists(argv[1]):
        query_from_file(argv[1])

    else:
        create_new_course(*argv)