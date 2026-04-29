# Import Playwright type for API work
from playwright.sync_api import Playwright


# Main class for handling all API requests
class APIClient:

    # Constructor runs automatically when object is created
    def __init__(self, playwright: Playwright, base_url):

        # Create reusable API request context using dynamic base URL
        self.api_context = playwright.request.new_context(
            base_url=base_url
        )

    # Method for GET request - fetch single user by ID
    def get_single_user(self, user_id):

        # Send GET request dynamically using user ID
        return self.api_context.get(
            f"/users/{user_id}"
        )

    # Method for POST request - create new post
    def create_post(self, title, body, user_id):

        # Send POST request with JSON body
        return self.api_context.post(
            "/posts",
            data={
                "title": title,
                "body": body,
                "userId": user_id
            }
        )

    # Method for closing API context after test ends
    def close_context(self):

        # Release resources and close session
        self.api_context.dispose()