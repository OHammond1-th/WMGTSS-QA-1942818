from Web_Data import models, wmgtss_qa
import create_user
from werkzeug.security import generate_password_hash, check_password_hash
import pytest


def set_database(database):
    create_user.set_database(database)


def user_create_test():
    create_user.create_new_user(1, "TestUser", "Test", "User", "2002-02-13", "Test")
    user = models.User.get_by_username("TestUser")
    assert user is not None
    return user


def user_get_by_id_test():
    user = user_create_test()
    user = models.User.get_by_id(user.ident)
    assert user is not None


def user_change_password_test():
    user = user_create_test()

    models.User.set_password_by_id(user.ident, generate_password_hash("NotTest"))
    user = models.User.get_by_id(user.ident)
    assert check_password_hash(user.password, "Test") is False

    models.User.set_password_by_id(user.ident, generate_password_hash("Test"))
    user = models.User.get_by_id(user.ident)
    assert check_password_hash(user.password, "Test") is True


if __name__ == "__main__":
    set_database(wmgtss_qa.db)

    # Tests
    user_create_test()
    user_get_by_id_test()
    user_change_password_test()
