"""
Test class for testing a failing setup because of returning False.
"""

from lily_unit_test.classification import Classification
from lily_unit_test.test_suite import TestSuite


class TestSetupFailReturnFalse(TestSuite):
    CLASSIFICATION = Classification.FAIL

    def setup(self):
        return False

    def test_dummy(self):
        return True


if __name__ == "__main__":

    TestSetupFailReturnFalse().run()
