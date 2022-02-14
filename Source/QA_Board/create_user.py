import re
from werkzeug.security import generate_password_hash
from postrgesql_api import DB_API
from sys import argv
from os.path import exists

database = None


def set_database(new_database):
    """
    Change the current database connection
    :param new_database:
    :return:
    """
    global database
    database = new_database


def get_role_id(role):
    """
    Returns the role id of the given role
    :param role: Role name
    :return: Role id
    """
    database.query(f"SELECT role_id FROM roles WHERE roles.role_name = '{role}'")
    return database.get_result(1)[0]


def create_new_user(role, username, firstname, lastname, dob, password=None):
    """
    Creates a new user in the database
    :param role: Role id
    :param username: The users username
    :param firstname: The users first name
    :param lastname: The users last name
    :param dob: The users date of birth
    :param password: The users password if given
    :return:
    """

    # if a password has been given hash it first
    if password:
        password = f"'{generate_password_hash(str(password))}'"
    else:
        password = 'NULL'

    database.query(
        f"INSERT INTO "
        f"users(role_id, user_username, user_password, user_firstname, user_lastname, user_dateofbirth) "
        f"VALUES "
        f"('{get_role_id(role)[0]}', '{str(username)}', {password}, '{str(firstname)}', '{str(lastname)}', '{str(dob)}') "
    )

    commit()


def query_from_file(file_path):
    """
    Iterate down a csv file and call create_new_user
    :param file_path: The file to iterate over
    :return:
    """
    lines = None

    # read lines into memory
    with open(file_path, 'r') as file:

        lines = file.readlines()

    try:
        # for each line create a new user
        for line in lines:
            line_args = line.split(',')

            create_new_user(*line_args)

    except ValueError as e:
        print(f"Args did not meet those required:\t{e}/5-6")
        database.rollback()


def commit():
    # manual database commit
    database.commit()


if __name__ == "__main__":

    database = DB_API("WMGTSS_QA_TEST", "administrator", "default")

    if exists(argv[1]):
        query_from_file(argv[1])

    else:
        create_new_user(*argv[1:])

