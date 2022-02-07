from postrgesql_api import DB_API
from sys import argv
from os.path import exists
import re

database = None


def set_database(cur_database):
    global database
    database = cur_database


def create_new_course(name, start, end=None):

    if end:
        end = str(end)

    database.query(
        f" INSERT INTO "
        f" courses(course_name, course_start, course_end) "
        f" VALUES "
        f" ({name}, {start}, {end}) "
    )


def query_from_file(file_path):

    lines = None

    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        for line in lines:

            line_args = re.split(r"(,|-|/|\s)+", line)

            create_course(*line_args)

        database.commit()

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/2-3")
        database.rollback()


if __name__ == "__main__":

    database = DB_API("WMGTSS_QA", "administrator", "default")

    if exists(argv[0]):
        query_from_file(argv[0])

    else:
        create_course(*argv)