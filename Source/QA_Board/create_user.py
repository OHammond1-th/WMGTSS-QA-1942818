import re

from postrgesql_api import DB_API
from datetime import datetime
from sys import argv
from os.path import exists

database = DB_API("WMGTSS_QA", "administrator", "default")


def get_role_id(role):
    database.query(f"SELECT 'role_id' FROM 'roles' WHERE 'role'('role_name') = {role}")
    return database.get_result()


def create_user(role, username, firstname, lastname, dob, password=None):

    if password:
        password = str(password)

    database.query(
        f"INSERT INTO "
        f"'users'('role_id', 'user_username', 'user_password', 'user_firstname', 'user_lastname', 'user_dateofbirth')"
        f"VALUES "
        f" ({int(role)}, {str(username)}, {password}, {firstname}, {lastname}, {dob}) "
    )


def query_from_file(file_path):

    lines = None

    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        for line in lines:

            line_args = re.split(r"(,|-|/|\s)+", line)
            line_args[0] = get_role_id(line_args[0])

            create_user(*line_args)

        database.commit()

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/6")
        database.rollback()


if __name__ == "__main__":

    if exists(argv[0]):
        query_from_file(argv[0])

    else:
        create_user(*argv)

