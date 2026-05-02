# Import pytest framework
import pytest

# Import JSON library for reading config files
import json

# Import Allure for reporting
import allure

# Import APIClient class for API testing
from API_Tests.api_client import APIClient

# Import AuthClient class for authentication testing
from API_Tests.auth_client import AuthClient

# Import LoginPage class for UI testing
from pages.login_page import LoginPage

# Import flaky analytics helpers
from utils.flaky_tracker import record_test, record_retry, save_report


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


# Fixture: Auth base URL
@pytest.fixture(scope="session")
def auth_base_url(env_config):

    # Return auth base URL from selected environment
    return env_config["auth_base_url"]


# Fixture: ReqRes API key
@pytest.fixture(scope="session")
def reqres_api_key(env_config):

    # Return ReqRes API key from selected environment
    return env_config["reqres_api_key"]


# Fixture: Auth email
@pytest.fixture(scope="session")
def auth_email(env_config):

    # Return auth email from selected environment
    return env_config["auth_email"]


# Fixture: Auth password
@pytest.fixture(scope="session")
def auth_password(env_config):

    # Return auth password from selected environment
    return env_config["auth_password"]


# Fixture: API client
@pytest.fixture(scope="session")
def api_client(playwright, api_base_url):

    # Create APIClient for public demo API
    return APIClient(
        playwright=playwright,
        base_url=api_base_url
    )


# Fixture: Auth client
@pytest.fixture(scope="session")
def auth_client(playwright, auth_base_url, reqres_api_key):

    # Create AuthClient for authentication API
    return AuthClient(
        playwright=playwright,
        auth_base_url=auth_base_url,
        api_key=reqres_api_key
    )


# Fixture: JWT token
@pytest.fixture(scope="session")
def jwt_token(auth_client, auth_email, auth_password):

    # Login through API/mock auth and return JWT token
    return auth_client.login_and_get_token(
        email=auth_email,
        password=auth_password
    )


# Fixture: Login page
@pytest.fixture
def login_page(page):

    # Create LoginPage object
    return LoginPage(page)


# Fixture: Authenticated page with JWT injected into localStorage
@pytest.fixture
def authenticated_page(page, ui_base_url, jwt_token):

    # Open UI base URL before setting localStorage
    page.goto(ui_base_url)

    # Inject JWT token into browser localStorage
    page.evaluate(
        """(token) => {
            localStorage.setItem("auth_token", token);
        }""",
        jwt_token
    )

    # Return browser page with injected token
    return page


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


# Hook: track test execution and retry events
def pytest_runtest_logreport(report):

    # Count only real test call phase
    if report.when == "call":

        # Record every final executed test
        if report.outcome in ["passed", "failed"]:
            record_test(report.nodeid)

        # Record retry event from pytest-rerunfailures
        if report.outcome == "rerun":
            record_retry(report.nodeid)


# Hook: save flaky analytics report at the end of pytest session
def pytest_sessionfinish(session, exitstatus):

    # Save flaky report to JSON file
    save_report()