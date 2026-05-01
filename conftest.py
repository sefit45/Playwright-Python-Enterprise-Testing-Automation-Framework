# Import pytest framework
import pytest

# Import JSON library for reading config files
import json

# Import Allure for reporting
import allure

# Import APIClient class for API testing
from API_Tests.api_client import APIClient

# Import LoginPage class for UI testing
from pages.login_page import LoginPage


# Add custom CLI option --env
def pytest_addoption(parser):

    # Add environment parameter to pytest command
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against"
    )


# Fixture: selected environment name
@pytest.fixture(scope="session")
def selected_env(request):

    # Return selected environment from command line
    return request.config.getoption("--env")


# Fixture: full environment config
@pytest.fixture(scope="session")
def env_config(selected_env):

    # Open environments configuration file
    with open("environments.json", "r") as file:

        # Load JSON content into Python dictionary
        environments = json.load(file)

    # Return selected environment configuration
    return environments[selected_env]


# Fixture: API base URL
@pytest.fixture(scope="session")
def api_base_url(env_config):

    # Return API base URL from selected environment
    return env_config["api_base_url"]


# Fixture: UI base URL
@pytest.fixture(scope="session")
def ui_base_url(env_config):

    # Return UI base URL from selected environment
    return env_config["ui_base_url"]


# Fixture: authentication token
@pytest.fixture(scope="session")
def auth_token(env_config):

    # Return authentication token from selected environment
    return env_config.get("auth_token")


# Fixture: API client
@pytest.fixture(scope="session")
def api_client(playwright, api_base_url, auth_token):

    # Create APIClient with Playwright, base URL and auth token
    return APIClient(
        playwright=playwright,
        base_url=api_base_url,
        token=auth_token
    )


# Fixture: Login page
@pytest.fixture
def login_page(page):

    # Create LoginPage object
    return LoginPage(page)


# Fixture: test data
@pytest.fixture(scope="session")
def test_data():

    # Open test data file
    with open("test_data.json", "r") as file:

        # Load JSON content into Python object
        return json.load(file)


# Hook: attach failure details
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # Execute test and get outcome
    outcome = yield

    # Get test report
    report = outcome.get_result()

    # Check only failed test execution phase
    if report.when == "call" and report.failed:

        # Attach failed test name to Allure
        allure.attach(
            item.name,
            name="Failed Test Name",
            attachment_type=allure.attachment_type.TEXT
        )

        # Try to get Playwright page object
        page = item.funcargs.get("page", None)

        # Attach screenshot only for UI tests
        if page:

            # Capture full page screenshot
            screenshot = page.screenshot(full_page=True)

            # Attach screenshot to Allure
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )