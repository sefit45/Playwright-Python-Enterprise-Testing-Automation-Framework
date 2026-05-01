# Import Playwright Page object for browser interaction
from playwright.sync_api import Page


# Page Object class for the Login screen
class LoginPage:

    # Constructor function - runs automatically when creating the class object
    def __init__(self, page: Page):

        # Save browser page object for internal use
        self.page = page

        # Selector for username input field
        self.username_input = "#username"

        # Selector for password input field
        self.password_input = "#password"

        # Selector for login button
        self.login_button = "button[type='submit']"

        # Selector for system flash message after login
        self.flash_message = "#flash"

    # Function for navigating to a given URL
    def goto(self, url):

        # Open the requested URL in browser
        self.page.goto(url)

    # Login function for system authentication
    def login(self, username, password):

        # Fill username field
        self.page.fill(self.username_input, username)

        # Fill password field
        self.page.fill(self.password_input, password)

        # Click Login button
        self.page.click(self.login_button)

    # Function that returns flash message element
    def get_flash_message(self):

        # Return locator for assertion validation
        return self.page.locator(self.flash_message)