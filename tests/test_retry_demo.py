# Import pytest library for test markers
import pytest


# Demo marker
# This test is used only to demonstrate retry mechanism behavior
@pytest.mark.demo
@pytest.mark.regression
def test_retry_demo_failure():

    # Expected value for demo validation
    expected_value = 10

    # Actual value is intentionally incorrect
    actual_value = 5

    # This assertion intentionally fails
    # This test should not run in normal CI regression execution
    assert actual_value == expected_value