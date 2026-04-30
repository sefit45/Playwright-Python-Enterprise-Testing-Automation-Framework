# Import pytest library for test markers
import pytest

# Import Allure library for professional reporting
import allure

# Import reusable API assertion helper functions
from API_Tests.assertions import (
    validate_status_code,
    validate_json_field,
    validate_field_exists
)

# Import reusable logger object
from utils.logger import logger


# API + Smoke + Regression test
# This test validates successful GET request for an existing user
@allure.feature("User API")
@allure.story("Get existing user")
@allure.title("Validate successful retrieval of an existing user by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_get_single_user(api_client, test_data):

    with allure.step("Read user ID from test data file"):
        user_id = test_data["api_tests"]["get_single_user"]["user_id"]

    with allure.step(f"Send GET request for user ID: {user_id}"):
        logger.info(f"Starting test: test_get_single_user")
        logger.info(f"Sending GET request for user ID: {user_id}")
        response = api_client.get_single_user(user_id)

    with allure.step("Validate HTTP status code is 200"):
        logger.info(f"Received status code: {response.status}")
        validate_status_code(response, 200)

    with allure.step("Convert response body to JSON"):
        response_body = response.json()

    with allure.step("Attach response body to Allure report"):
        allure.attach(
            str(response_body),
            name="GET User Response Body",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validate returned user ID"):
        validate_json_field(response_body, "id", user_id)

    with allure.step("Validate username exists"):
        validate_field_exists(response_body, "username")

    with allure.step("Validate email exists"):
        validate_field_exists(response_body, "email")

    logger.info(f"Test completed successfully: test_get_single_user")


# API + Negative + Regression test
# This test validates API behavior for non-existing user
@allure.feature("User API")
@allure.story("Get non-existing user")
@allure.title("Validate 404 response for non-existing user")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_get_non_existing_user(api_client):

    non_existing_user_id = 99999

    with allure.step(f"Send GET request for non-existing user ID: {non_existing_user_id}"):
        logger.info(f"Starting test: test_get_non_existing_user")
        logger.info(f"Sending GET request for non-existing user ID: {non_existing_user_id}")
        response = api_client.get_single_user(non_existing_user_id)

    with allure.step("Validate HTTP status code is 404"):
        logger.info(f"Received status code: {response.status}")
        validate_status_code(response, 404)

    with allure.step("Attach empty response body to Allure report"):
        allure.attach(
            response.text(),
            name="GET Non Existing User Response Body",
            attachment_type=allure.attachment_type.JSON
        )

    logger.info(f"Test completed successfully: test_get_non_existing_user")


# API + Smoke + Regression test
# This test validates successful POST request for creating a new post
@allure.feature("Post API")
@allure.story("Create new post")
@allure.title("Validate successful creation of a new post")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client):

    title = "QA Automation"
    body = "Playwright API test"
    user_id = 1

    with allure.step("Prepare POST request test data"):
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }

    with allure.step("Attach request payload to Allure report"):
        allure.attach(
            str(payload),
            name="POST Request Payload",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Send POST request to create a new post"):
        logger.info(f"Starting test: test_create_post")
        logger.info(f"Sending POST request with title: {title}")
        response = api_client.create_post(
            title=title,
            body=body,
            user_id=user_id
        )

    with allure.step("Validate HTTP status code is 201"):
        logger.info(f"Received status code: {response.status}")
        validate_status_code(response, 201)

    with allure.step("Convert response body to JSON"):
        response_body = response.json()

    with allure.step("Attach response body to Allure report"):
        allure.attach(
            str(response_body),
            name="POST Response Body",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validate returned title value"):
        validate_json_field(response_body, "title", title)

    with allure.step("Validate returned body value"):
        validate_json_field(response_body, "body", body)

    with allure.step("Validate returned user ID"):
        validate_json_field(response_body, "userId", user_id)

    logger.info(f"Test completed successfully: test_create_post")