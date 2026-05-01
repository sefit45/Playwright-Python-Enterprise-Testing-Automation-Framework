# Import Playwright type for API work
from playwright.sync_api import Playwright

# Import Allure for reporting token details
import allure

# Import base64 for JWT-like encoding
import base64

# Import JSON library for converting dictionaries to JSON strings
import json

# Import time library for token timestamp
import time

# Import central logger
from utils.logger import logger


# Client dedicated to authentication API flows
class AuthClient:

    # Constructor creates a dedicated API context for auth operations
    def __init__(self, playwright: Playwright, auth_base_url, api_key):

        # Save auth base URL for logging
        self.auth_base_url = auth_base_url

        # Save API key for future real API authentication
        self.api_key = api_key

        # Create headers for future real authentication API requests
        self.headers = {
            "Content-Type": "application/json",
            "x-api-key": api_key
        }

        # Create Playwright API context for future auth requests
        self.api_context = playwright.request.new_context(
            base_url=auth_base_url,
            extra_http_headers=self.headers
        )

    # Generate mock JWT token for stable framework testing
    def login_and_get_token(self, email, password):

        # Log mock JWT generation
        logger.info("Generating mock JWT token for stable test execution")

        # Create JWT header
        header = {
            "alg": "HS256",
            "typ": "JWT"
        }

        # Create JWT payload
        payload = {
            "sub": email,
            "role": "user",
            "iat": int(time.time())
        }

        # Encode JWT header
        header_encoded = base64.urlsafe_b64encode(
            json.dumps(header).encode()
        ).decode().rstrip("=")

        # Encode JWT payload
        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip("=")

        # Create mock signature
        signature = "mock-signature"

        # Build JWT-like token
        token = f"{header_encoded}.{payload_encoded}.{signature}"

        # Attach generated token to Allure report
        allure.attach(
            token,
            name="Generated Mock JWT",
            attachment_type=allure.attachment_type.TEXT
        )

        # Return token to fixture or test
        return token

    # Close auth API context
    def close_context(self):

        # Log context closing
        logger.info("Closing Auth API context")

        # Dispose Playwright API context
        self.api_context.dispose()