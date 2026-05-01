# Import pytest for test markers
import pytest

# Import Allure for reporting
import allure

# Import custom validation utilities
from API_Tests.assertions import (
    validate_status_code,
    validate_json_field,
    validate_field_exists
)

# Import logger for execution logs
from utils.logger import logger


# =========================================================
# Test: Get existing user
# =========================================================
@allure.feature("User API")
@allure.story("Get existing user")
@allure.title("Validate successful retrieval of an existing user by ID")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_get_single_user(api_client, test_data):

    # Get test data from JSON
    user_id = test_data["api_tests"]["get_single_user"]["user_id"]

    # Log test start
    logger.info("Starting test_get_single_user")

    # Send GET request via API client
    response = api_client.get_single_user(user_id)

    # Validate status code
    validate_status_code(response, 200)

    # Convert response to JSON
    response_body = response.json()

    # Validate response fields
    validate_json_field(response_body, "id", user_id)
    validate_field_exists(response_body, "username")
    validate_field_exists(response_body, "email")


# =========================================================
# Test: Get non-existing user
# =========================================================
@allure.feature("User API")
@allure.story("Get non-existing user")
@allure.title("Validate 404 response for non-existing user")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.negative
@pytest.mark.regression
def test_get_non_existing_user(api_client):

    # Define non-existing user ID
    non_existing_user_id = 99999

    # Log test start
    logger.info("Starting test_get_non_existing_user")

    # Send GET request
    response = api_client.get_single_user(non_existing_user_id)

    # Validate 404 response
    validate_status_code(response, 404)


# =========================================================
# Test: Create new post
# =========================================================
@allure.feature("Post API")
@allure.story("Create new post")
@allure.title("Validate successful creation of a new post")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client, test_data):

    # Get test data from JSON
    post_data = test_data["api_tests"]["create_post"]

    title = post_data["title"]
    body = post_data["body"]
    user_id = post_data["user_id"]

    # Log test start
    logger.info("Starting test_create_post")

    # Send POST request via API client
    response = api_client.create_post(
        title=title,
        body=body,
        user_id=user_id
    )

    # Validate status code
    validate_status_code(response, 201)

    # Convert response to JSON
    response_body = response.json()

    # Validate response fields
    validate_json_field(response_body, "title", title)
    validate_json_field(response_body, "body", body)
    validate_json_field(response_body, "userId", user_id)