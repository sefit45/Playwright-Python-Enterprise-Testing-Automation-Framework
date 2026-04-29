# Pytest library - ספריית pytest להרצת בדיקות
import pytest

# JSON library - ספרייה לקריאת נתוני בדיקה מקובץ JSON
import json

# Playwright expect - מנגנון בדיקות ואימותים של Playwright
from playwright.sync_api import expect


# Load test data from JSON file - טעינת נתוני בדיקה מקובץ JSON
def load_test_data():

    # Open test data file - פתיחת קובץ נתוני הבדיקה
    with open("test_data.json", "r") as file:

        # Return JSON content as Python object - החזרת תוכן הקובץ כאובייקט Python
        return json.load(file)


# Data driven login test - בדיקת Login מבוססת נתונים
@pytest.mark.parametrize("data", load_test_data())
def test_login_from_json(login_page, base_url, data):

    # Open login page using base URL - פתיחת מסך ההתחברות לפי הסביבה שנבחרה
    login_page.goto(base_url + "/login")

    # Perform login action - ביצוע התחברות עם המשתמש והסיסמה מה-JSON
    login_page.login(
        data["username"],
        data["password"]
    )

    # Validate expected message - בדיקה שהודעת התוצאה תואמת לצפוי
    expect(login_page.get_flash_message()).to_contain_text(
        data["expected"]
    )