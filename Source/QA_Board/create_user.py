import re
from werkzeug.security import generate_password_hash
from postrgesql_api import DB_API
from sys import argv
from os.path import exists

database = None


def set_database(cur_database):
    global database
    database = cur_database


def get_role_id(role):
    database.query(f"SELECT role_id FROM roles WHERE roles.role_name = '{role}'")
    return database.get_result(1)[0]


def create_new_user(role, username, firstname, lastname, dob, password=None):

    if password:
        password = generate_password_hash(str(password))

    database.query(
        f"INSERT INTO "
        f"users(role_id, user_username, user_password, user_firstname, user_lastname, user_dateofbirth) "
        f"VALUES "
        f"('{role}', '{str(username)}', '{password}', '{str(firstname)}', '{str(lastname)}', '{str(dob)}') "
    )


def query_from_file(file_path):

    lines = None

    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        for line in lines:
            line_args = line[:-2].split(',')
            line_args[0] = get_role_id(line_args[0])[0]

            print(line_args)

            create_new_user(*line_args)

        commit()

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/5-6")
        database.rollback()


def commit():
    database.commit()


if __name__ == "__main__":

    database = DB_API("WMGTSS_QA_TEST", "administrator", "default")

    if exists(argv[1]):
        query_from_file(argv[1])

    else:
        create_new_user(*argv[1:])

    database.commit()

