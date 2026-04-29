# Import pytest library for test markers
import pytest


# Retry demo test
# This test is intentionally designed to fail
# so we can verify that pytest-rerunfailures works correctly
@pytest.mark.regression
def test_retry_demo_failure():

    # Expected value for demo validation
    expected_value = 10

    # Actual value is intentionally incorrect
    actual_value = 5

    # This assertion will fail on purpose
    # Pytest should automatically retry this test based on pytest.ini settings
    assert actual_value == expected_value
    