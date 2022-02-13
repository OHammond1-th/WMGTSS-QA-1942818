from Web_Data import test_website
import cProfile


class TestHarness:

    def __init__(self, web_side=False):
        if web_side:
            self.app = test_website()
            self.test_suite = []

    def add_tests(self, *funcs):
        for test in funcs:
            self.test_suite.append(test)

    def run(self):
        for test in self.test_suite:
            test()

    def get_tests(self):
        return self.test_suite


if __name__ == "__main__":
    from Backend import backend_harness
    test_harness = TestHarness(True)

    test_harness.add_tests(backend_harness.BackendHarness().get_tests())

    cProfile.run("test_harness.run()")
