from playwright.sync_api import expect
import pytest
import allure

from API_Tests.assertions import validate_status_code
from utils.logger import logger


@allure.feature("Full Stack Auth")
@allure.story("API login + UI session reuse")
@allure.title("Validate API login and skip UI login using session injection")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.fullstack
@pytest.mark.api
@pytest.mark.ui
@pytest.mark.regression
def test_api_login_and_ui_session(api_client, authenticated_page, ui_base_url):

    logger.info("Starting API + UI session injection test")

    # Step 1: API readiness (simulate login)
    with allure.step("Validate API login / readiness"):
        response = api_client.get_single_user(1)
        validate_status_code(response, 200)

    # Step 2: Navigate to secure page directly
    with allure.step("Open secure page without UI login"):
        authenticated_page.goto(ui_base_url + "/secure")

    # Step 3: Validate we are "logged in"
    with allure.step("Validate secure page access"):
        expect(authenticated_page.locator("#flash")).to_be_visible()