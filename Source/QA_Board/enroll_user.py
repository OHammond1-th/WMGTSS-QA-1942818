from postrgesql_api import DB_API
from sys import argv
from os.path import exists
import re

database = None


def set_database(cur_database):
    global database
    database = cur_database


def create_new_enrollment(course, user):

    database.query(
        f" INSERT INTO "
        f" enrollments(course_id, user_id) "
        f" VALUES "
        f" ({course}, {user}) "
    )


def query_from_file(file_path):

    lines = None

    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        for line in lines:
            line_args = line[:-2].split(',')

            create_new_enrollment(*line_args)

        database.commit()

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/2-3")
        database.rollback()


if __name__ == "__main__":

    database = DB_API("WMGTSS_QA_TEST", "administrator", "default")

    if exists(argv[1]):
        query_from_file(argv[1])

    else:
        create_new_enrollment(*argv)
