from Web_Data import models, wmgtss_qa
import create_course
import pytest


def set_database(database):
    create_course.set_database(database)


def course_create_test():
    create_course.create_new_course("WMGTEST", "2020-01-01", "2024-01-01")
    course = models.Course.get_by_name("WMGTEST")
    assert course is not None
    return course


if __name__ == "__main__":
    set_database(wmgtss_qa.db)

    # Tests
    course_create_test()

