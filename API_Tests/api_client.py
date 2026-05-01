# Import Playwright type for API work
from playwright.sync_api import Playwright

# Import Allure for attaching request and response details to the report
import allure

# Import time library for retry delay
import time

# Import central logger for execution logs
from utils.logger import logger


# Main class for handling all API requests
class APIClient:

    # Constructor runs automatically when object is created
    def __init__(self, playwright: Playwright, base_url, token=None):

        # Save base URL
        self.base_url = base_url

        # Save optional token for authentication
        self.token = token

        # Define default headers
        self.headers = {
            "Content-Type": "application/json"
        }

        # If token exists, add Authorization header
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

        # Retry configuration
        self.retry_status_codes = [500, 502, 503, 504]
        self.max_retries = 3
        self.retry_delay_seconds = 1

        # Create API request context with headers
        self.api_context = playwright.request.new_context(
            base_url=base_url,
            extra_http_headers=self.headers
        )

    # Attach response to Allure
    def _attach_response_to_allure(self, response, name):

        allure.attach(
            str(response.status),
            name=f"{name} - Status Code",
            attachment_type=allure.attachment_type.TEXT
        )

        allure.attach(
            response.text(),
            name=f"{name} - Response Body",
            attachment_type=allure.attachment_type.JSON
        )

    # Retry mechanism
    def _send_with_retry(self, request_function, endpoint, request_name, **kwargs):

        for attempt in range(1, self.max_retries + 1):

            logger.info(
                f"{request_name} | Attempt {attempt}/{self.max_retries} | "
                f"URL: {self.base_url}{endpoint}"
            )

            response = request_function(endpoint, **kwargs)

            if response.status not in self.retry_status_codes:

                logger.info(
                    f"{request_name} | Status: {response.status} | No retry needed"
                )

                self._attach_response_to_allure(response, request_name)

                return response

            logger.warning(
                f"{request_name} | Retryable status code: {response.status}"
            )

            if attempt < self.max_retries:
                time.sleep(self.retry_delay_seconds)

        self._attach_response_to_allure(
            response,
            f"{request_name} - Final Failed"
        )

        return response

    # GET user
    def get_single_user(self, user_id):

        endpoint = f"/users/{user_id}"

        return self._send_with_retry(
            request_function=self.api_context.get,
            endpoint=endpoint,
            request_name="GET Single User"
        )

    # POST create
    def create_post(self, title, body, user_id):

        endpoint = "/posts"

        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }

        allure.attach(
            str(payload),
            name="POST Payload",
            attachment_type=allure.attachment_type.JSON
        )

        return self._send_with_retry(
            request_function=self.api_context.post,
            endpoint=endpoint,
            request_name="POST Create Post",
            data=payload
        )

    # Close context
    def close_context(self):

        logger.info("Closing API context")

        self.api_context.dispose()