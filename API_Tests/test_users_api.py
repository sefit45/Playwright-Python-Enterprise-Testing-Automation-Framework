import pytest
import allure

from API_Tests.assertions import (
    validate_status_code,
    validate_json_field,
    validate_field_exists
)

from utils.logger import logger


@allure.feature("User API")
@allure.story("Get existing user")
@allure.title("Validate successful retrieval of an existing user by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_get_single_user(api_client, test_data):

    user_id = test_data["api_tests"]["get_single_user"]["user_id"]

    with allure.step(f"Send GET request for user ID: {user_id}"):
        logger.info("Starting test_get_single_user")
        response = api_client.get_single_user(user_id)

    with allure.step("Attach API response"):
        allure.attach(
            response.text(),
            name="GET Single User Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validate status code is 200"):
        validate_status_code(response, 200)

    response_body = response.json()

    with allure.step("Validate returned user ID"):
        validate_json_field(response_body, "id", user_id)

    with allure.step("Validate username exists"):
        validate_field_exists(response_body, "username")

    with allure.step("Validate email exists"):
        validate_field_exists(response_body, "email")


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
        logger.info("Starting test_get_non_existing_user")
        response = api_client.get_single_user(non_existing_user_id)

    with allure.step("Attach API response"):
        allure.attach(
            response.text(),
            name="GET Non Existing User Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validate status code is 404"):
        validate_status_code(response, 404)


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

    payload = {
        "title": title,
        "body": body,
        "userId": user_id
    }

    with allure.step("Attach request payload"):
        allure.attach(
            str(payload),
            name="POST Request Payload",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Send POST request"):
        logger.info("Starting test_create_post")
        response = api_client.create_post(
            title=title,
            body=body,
            user_id=user_id
        )

    with allure.step("Attach API response"):
        allure.attach(
            response.text(),
            name="POST Response",
            attachment_type=allure.attachment_type.JSON
        )

    with allure.step("Validate status code is 201"):
        validate_status_code(response, 201)

    response_body = response.json()

    with allure.step("Validate returned title"):
        validate_json_field(response_body, "title", title)

    with allure.step("Validate returned body"):
        validate_json_field(response_body, "body", body)

    with allure.step("Validate returned user ID"):
        validate_json_field(response_body, "userId", user_id)