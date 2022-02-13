from . import user_tests, course_tests, question_tests, comment_tests
from Testing import test_harness


class BackendHarness(test_harness.TestHarness):

    def __init__(self):
        super().__init__(False)
        self.test_suite = [
            user_tests.user_create_test,
            user_tests.user_get_by_id_test,
            user_tests.user_change_password_test(),

        ]
