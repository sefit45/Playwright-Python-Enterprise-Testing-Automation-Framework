import json
import pytest
import allure

from API_Tests.api_client import APIClient


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        help="Environment to run tests against: dev, st, uat, prod"
    )


@pytest.fixture(scope="session")
def selected_env(request):
    return request.config.getoption("--env")


@pytest.fixture(scope="session")
def base_url(selected_env):
    with open("environments.json", "r") as file:
        environments = json.load(file)

    return environments[selected_env]


@pytest.fixture(scope="session")
def api_client(base_url):
    return APIClient(base_url)


@pytest.fixture(scope="session")
def test_data():
    with open("test_data.json", "r") as file:
        return json.load(file)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attach useful debugging information to Allure when a test fails.
    Works safely for both UI tests and API tests.
    """

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