# Import pytest for test markers
import pytest

# Import Allure for structured reporting
import allure

# Import Playwright expect for UI assertions
from playwright.sync_api import expect

# Import logger for execution logs
from utils.logger import logger


# =========================================================
# Test: Inject JWT token into UI session
# =========================================================
@allure.feature("JWT UI Session")
@allure.story("Inject JWT into browser localStorage")
@allure.title("Validate JWT token injection into UI session")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.auth
@pytest.mark.ui
@pytest.mark.fullstack
@pytest.mark.regression
def test_jwt_token_injected_to_ui_session(authenticated_page, jwt_token):

    # Log test start
    logger.info("Starting JWT UI session injection test")

    # Read JWT token from browser localStorage
    stored_token = authenticated_page.evaluate(
        """() => {
            return localStorage.getItem("auth_token");
        }"""
    )

    # Validate token exists in browser localStorage
    assert stored_token is not None

    # Validate stored token equals generated JWT token
    assert stored_token == jwt_token

    # Validate page is available
    expect(authenticated_page).to_have_title("The Internet")