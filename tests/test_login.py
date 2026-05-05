import pytest
import json
import allure
from playwright.sync_api import expect


def load_test_data():
    with open("test_data.json", "r") as file:
        data = json.load(file)
        return data["ui_tests"]   # ✅ הפתרון


@allure.feature("UI Login")
@allure.story("Login using JSON test data")
@allure.title("Validate login from JSON data")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("data", load_test_data())
def test_login_from_json(login_page, ui_base_url, data):

    login_page.goto(ui_base_url + "/login")

    login_page.login(
        data["username"],
        data["password"]
    )

    expect(login_page.get_flash_message()).to_contain_text(
        data["expected"]
    )