# Import pytest framework
import pytest

# Import JSON library for reading config files
import json

# Import Allure for reporting
import allure

# Import APIClient class for API testing
from API_Tests.api_client import APIClient


# ================================
# Add custom CLI option --env
# ================================
def pytest_addoption(parser):
    """
    Adds custom command line option:
    Example:
        pytest --env=dev
        pytest --env=prod
    """
    parser.addoption(
        "--env",                # CLI parameter name
        action="store",         # Store the value
        default="dev",          # Default value if not provided
        help="Environment to run tests against"
    )


# ================================
# Fixture: Selected Environment
# ================================
@pytest.fixture(scope="session")
def selected_env(request):
    """
    Reads the environment value from CLI
    """
    return request.config.getoption("--env")


# ================================
# Fixture: Base URL
# ================================
@pytest.fixture(scope="session")
def base_url(selected_env):
    """
    Loads base URL from environments.json
    according to selected environment
    """
    with open("environments.json", "r") as file:
        environments = json.load(file)

    return environments[selected_env]


# ================================
# Fixture: API Client (FIXED VERSION)
# ================================
@pytest.fixture(scope="session")
def api_client(playwright, base_url):
    """
    Creates API client instance
    IMPORTANT: Pass both playwright and base_url
    """
    return APIClient(playwright, base_url)


# ================================
# Fixture: Test Data
# ================================
@pytest.fixture(scope="session")
def test_data():
    """
    Loads test data from JSON file
    """
    with open("test_data.json", "r") as file:
        return json.load(file)


# ================================
# Hook: Attach failure details
# ================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach useful debugging information to Allure
    Works for both UI and API tests
    """

    outcome = yield
    report = outcome.get_result()

    # Only act on test failure during execution phase
    if report.when == "call" and report.failed:

        # Attach test name
        allure.attach(
            item.name,
            name="Failed Test Name",
            attachment_type=allure.attachment_type.TEXT
        )

        # Try to get Playwright page (only for UI tests)
        page = item.funcargs.get("page", None)

        if page:
            screenshot = page.screenshot(full_page=True)

            # Attach screenshot to Allure
            allure.attach(
                screenshot,
                name="Failure Screenshot",
                attachment_type=allure.attachment_type.PNG
            )