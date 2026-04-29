# Pytest library for fixtures and hooks
import pytest

# JSON library for reading JSON files
import json

# OS library for reading environment variables
import os

# Load variables from .env file
from dotenv import load_dotenv

# Import Login Page Object
from pages.login_page import LoginPage

# Import API Client
from API_Tests.api_client import APIClient


# Load all variables from .env file at framework startup
load_dotenv()


# =========================================================
# Add custom CLI option --env
#
# Example:
# pytest --env=dev
# pytest --env=prod
# =========================================================
def pytest_addoption(parser):
    parser.addoption(
        "--env",                    # Parameter name
        action="store",             # Store value
        default="dev",              # Default value
        help="Environment name"     # Help text
    )


# =========================================================
# Base URL fixture
# Load URL from environments.json
# according to selected environment
# =========================================================
@pytest.fixture(scope="session")
def base_url(request):

    # Get selected environment name
    env_name = request.config.getoption("--env")

    # Open environments file
    with open("environments.json", "r") as file:
        environments = json.load(file)

    # Return selected environment URL
    return environments[env_name]


# =========================================================
# Test Data fixture
# Load test data from test_data.json
# =========================================================
@pytest.fixture(scope="session")
def test_data():

    # Open test data file
    with open("test_data.json", "r") as file:
        data = json.load(file)

    # Return all test data
    return data


# =========================================================
# Secret Data fixture
# Load sensitive values from .env file
# =========================================================
@pytest.fixture(scope="session")
def secret_data():

    # Return all secret values from environment variables
    return {
        "app_username": os.getenv("APP_USERNAME"),
        "app_password": os.getenv("APP_PASSWORD"),
        "api_token": os.getenv("API_TOKEN"),
        "db_username": os.getenv("DB_USERNAME"),
        "db_password": os.getenv("DB_PASSWORD")
    }


# =========================================================
# Login Page fixture
# Create LoginPage object for each UI test
# =========================================================
@pytest.fixture
def login_page(page):

    # Return LoginPage object
    return LoginPage(page)


# =========================================================
# API Client fixture
# Create APIClient object for API tests
# using dynamic base_url from environments.json
# =========================================================
@pytest.fixture
def api_client(playwright, base_url):

    # Create API client before test starts
    client = APIClient(
        playwright,
        base_url
    )

    # Send the client object to the test
    yield client

    # Close API context after test ends
    client.close_context()


# =========================================================
# Screenshot on failure hook
# Take automatic screenshot when UI test fails
# =========================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    # Execute test
    outcome = yield

    # Get test result
    report = outcome.get_result()

    # Check if test failed during execution
    if report.when == "call" and report.failed:

        # Get page object from test
        page = item.funcargs.get("page")

        # If page exists
        if page:

            # Take screenshot
            page.screenshot(
                path="failure_screenshot.png"
            )