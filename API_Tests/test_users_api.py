
# Import pytest library for test markers
import pytest

# Import reusable API assertion helper functions
from API_Tests.assertions import (
    validate_status_code,     # Validate HTTP status code
    validate_json_field,      # Validate exact field value inside JSON
    validate_field_exists     # Validate field exists and is not empty
)

# Import reusable logger object
from utils.logger import logger


# Smoke + API + Regression test
# This test validates successful GET request for existing user
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_get_single_user(api_client, test_data):

    # Get user ID from test_data.json file
    user_id = test_data["api_tests"]["get_single_user"]["user_id"]

    # Log test start
    logger.info("Starting test: test_get_single_user")

    # Log request details
    logger.info(f"Sending GET request for user ID: {user_id}")

    # Send GET request using reusable API client
    response = api_client.get_single_user(user_id)

    # Log received status code
    logger.info(f"Received status code: {response.status}")

    # Validate HTTP status code is 200
    validate_status_code(response, 200)

    # Convert response body to JSON format
    response_body = response.json()

    # Validate returned user ID
    validate_json_field(response_body, "id", user_id)

    # Validate username field exists
    validate_field_exists(response_body, "username")

    # Validate email field exists
    validate_field_exists(response_body, "email")

    # Log successful test completion
    logger.info("Test completed successfully: test_get_single_user")


# Negative + API + Regression test
# This test validates response for non-existing user
@pytest.mark.regression
@pytest.mark.api
@pytest.mark.negative
def test_get_non_existing_user(api_client):

    # Define fake user ID that does not exist
    non_existing_user_id = 99999

    # Log test start
    logger.info("Starting test: test_get_non_existing_user")

    # Log request details
    logger.info(
        f"Sending GET request for non-existing user ID: {non_existing_user_id}"
    )

    # Send GET request using fake ID
    response = api_client.get_single_user(non_existing_user_id)

    # Log received status code
    logger.info(f"Received status code: {response.status}")

    # Validate expected status code for non-existing user
    validate_status_code(response, 404)

    # Log successful test completion
    logger.info("Test completed successfully: test_get_non_existing_user")


# Smoke + API + Regression test
# This test validates successful POST request for new post creation
@pytest.mark.smoke
@pytest.mark.api
@pytest.mark.regression
def test_create_post(api_client, test_data):

    # Get post data from test_data.json file
    post_data = test_data["api_tests"]["create_post"]

    # Log test start
    logger.info("Starting test: test_create_post")

    # Log request details
    logger.info(f"Sending POST request with title: {post_data['title']}")

    # Send POST request using reusable API client
    response = api_client.create_post(
        title=post_data["title"],       # Post title
        body=post_data["body"],         # Post body content
        user_id=post_data["user_id"]    # Related user ID
    )

    # Log received status code
    logger.info(f"Received status code: {response.status}")

    # Validate HTTP status code is 201
    validate_status_code(response, 201)

    # Convert response body to JSON format
    response_body = response.json()

    # Validate returned title value
    validate_json_field(response_body, "title", post_data["title"])

    # Validate returned body value
    validate_json_field(response_body, "body", post_data["body"])

    # Validate returned user ID
    validate_json_field(response_body, "userId", post_data["user_id"])

    # Log successful test completion
    logger.info("Test completed successfully: test_create_post")