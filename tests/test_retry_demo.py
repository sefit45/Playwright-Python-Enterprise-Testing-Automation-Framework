# Import pytest library for test markers
import pytest


# Demo test used only to demonstrate retry behavior
# This test intentionally fails and should be excluded from normal CI execution
@pytest.mark.demo
@pytest.mark.regression
def test_retry_demo_failure():

    # Expected value for demo validation
    expected_value = 10

    # Actual value is intentionally incorrect
    actual_value = 5

    # This assertion intentionally fails
    # CI excludes this test using: not demo
    assert actual_value == expected_value