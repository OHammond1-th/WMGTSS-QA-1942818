import re
from werkzeug.security import generate_password_hash
from postrgesql_api import DB_API
from sys import argv
from os.path import exists

database = DB_API("WMGTSS_QA", "administrator", "default")


def get_role_id(role):
    database.query(f"SELECT role_id FROM roles WHERE roles.role_name = '{role}'")
    return database.get_result(1)[0]


def create_user(role, username, firstname, lastname, dob, password=None):

    if password:
        password = str(password)

    database.query(
        f"INSERT INTO "
        f"users(role_id, user_username, user_password, user_firstname, user_lastname, user_dateofbirth)"
        f" VALUES "
        f"('{get_role_id(role)}', '{str(username)}', '{generate_password_hash(password)}', '{str(firstname)}', '{str(lastname)}', '{str(dob)}') "
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
        print(f"Args did not meet those required:\t{e}/5-6")
        database.rollback()


if __name__ == "__main__":

    if exists(argv[1]):
        query_from_file(argv[1])

    else:
        create_user(*argv[1:])

    database.commit()

