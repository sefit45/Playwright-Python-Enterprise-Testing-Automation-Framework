from playwright.sync_api import expect
import pytest
import allure

from API_Tests.assertions import validate_status_code
from utils.logger import logger


@allure.feature("Full Stack QA Automation")
@allure.story("API and UI validation in one flow")
@allure.title("Validate API availability before successful UI login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.fullstack
@pytest.mark.ui
@pytest.mark.api
@pytest.mark.regression
def test_api_readiness_before_ui_login(api_client, login_page, ui_base_url):

    username = "tomsmith"
    password = "SuperSecretPassword!"
    api_user_id = 1

    logger.info("Starting full stack test")

    with allure.step("Validate API readiness"):
        response = api_client.get_single_user(api_user_id)
        validate_status_code(response, 200)

    with allure.step("Open UI login page"):
        login_page.goto(ui_base_url + "/login")

    with allure.step("Perform login"):
        login_page.login(username, password)

    with allure.step("Validate login success"):
        expect(login_page.get_flash_message()).to_contain_text(
            "You logged into a secure area!"
        )