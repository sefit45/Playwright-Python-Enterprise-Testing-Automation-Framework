# Import pytest for test markers
import pytest

# Import Allure for structured reporting
import allure


# =========================================================
# Test: Real API login and JWT token extraction
# =========================================================
@allure.feature("Authentication API")
@allure.story("JWT token generation")
@allure.title("Validate successful API login and JWT token extraction")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
@pytest.mark.auth
@pytest.mark.regression
def test_login_and_get_jwt_token(jwt_token):

    # Validate token exists
    assert jwt_token is not None

    # Validate token is string
    assert isinstance(jwt_token, str)

    # Validate token is not empty
    assert len(jwt_token) > 0