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


def create_new_enrollment(course, user):
    """
    Creates a new enrollment in the database
    :param course: The course id
    :param user: The user id
    :return:
    """
    database.query(
        f" INSERT INTO "
        f" enrollments(course_id, user_id) "
        f" VALUES "
        f" ({course}, {user}) "
    )


def query_from_file(file_path):
    """
    Iterate down a csv file and call create_new_enrollment
    :param file_path: The file to iterate over
    :return:
    """
    lines = None

    # read the file into memory
    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        # for each line create an enrollment
        for line in lines:
            line_args = line[:-1].split(',')

            create_new_enrollment(*line_args)

            commit()

    except ValueError as e:
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
        create_new_enrollment(*argv)
