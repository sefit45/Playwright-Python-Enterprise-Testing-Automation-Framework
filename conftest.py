import pytest
import json
import allure

from API_Tests.api_client import APIClient
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against"
    )


@pytest.fixture(scope="session")
def selected_env(request):
    return request.config.getoption("--env")


# ================================
# NEW: full environment config
# ================================
@pytest.fixture(scope="session")
def env_config(selected_env):
    with open("environments.json", "r") as file:
        environments = json.load(file)

    return environments[selected_env]


# ================================
# API BASE URL
# ================================
@pytest.fixture(scope="session")
def api_base_url(env_config):
    return env_config["api_base_url"]


# ================================
# UI BASE URL
# ================================
@pytest.fixture(scope="session")
def ui_base_url(env_config):
    return env_config["ui_base_url"]


# ================================
# API CLIENT
# ================================
@pytest.fixture(scope="session")
def api_client(playwright, api_base_url):
    return APIClient(playwright, api_base_url)


# ================================
# LOGIN PAGE
# ================================
@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture(scope="session")
def test_data():
    with open("test_data.json", "r") as file:
        return json.load(file)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:

        allure.attach(
            item.name,
            name="Failed Test Name",
            attachment_type=allure.attachment_type.TEXT
        )

        page = item.funcargs.get("page", None)

        if page:
            screenshot = page.screenshot(full_page=True)

            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )