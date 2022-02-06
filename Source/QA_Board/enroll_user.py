from postrgesql_api import DB_API
from sys import argv
from os.path import exists
import re

database = DB_API("WMGTSS_QA", "administrator", "default")


def create_course(course, user):

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

            line_args = re.split(r"(,|-|/|\s)+", line)

            create_course(*line_args)

        database.commit()

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/2-3")
        database.rollback()


if __name__ == "__main__":

    if exists(argv[0]):
        query_from_file(argv[0])

    else:
        create_course(*argv)