import unittest


def simple_test():
    assert 1 + 1 == 2


def failing_test():
    assert 1 + 1 == 3


class MyTestCase(unittest.TestCase):
    def test_function(self):
        self.assertIsNone(simple_test())


# Wrap the simple test function in a FunctionTestCase
# wrapped_simple_test = unittest.FunctionTestCase(simple_test)
# wrapped_failing_test = unittest.FunctionTestCase(failing_test)

# Add to a test suite
suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(MyTestCase))
# suite.addTest(wrapped_simple_test)
# suite.addTest(wrapped_failing_test)

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite)
