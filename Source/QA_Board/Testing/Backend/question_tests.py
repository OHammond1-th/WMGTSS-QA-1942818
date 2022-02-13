from Web_Data import models, wmgtss_qa
import pytest


def create_question_test():
    user = models.User.get_random()
    course = models.Course.get_random()
    question = models.Question.create_question(course.ident, user.ident,
                                               "This is a test", "Did you know this is a test", True)
    assert question is not None
    return question


def answer_question_test():
    question = create_question_test()
    models.Question.provide_answer(question.ident, "Yes this is a test")
    question = models.Question.get_question_by_id(question.ident)

    assert question.answer == "Yes this is a test"


if __name__ == "__main__":

    # Tests
    create_question_test()
    answer_question_test()
