# Import JSON library for report creation
import json

# Import OS library for folder and environment variable handling
import os


# Central dictionary for flaky test analytics
flaky_data = {
    "total_tests": 0,
    "retried_tests": 0,
    "flaky_tests": [],
    "retry_count": {}
}


# Record every executed test
def record_test(test_name):

    # Increase total executed tests counter
    flaky_data["total_tests"] += 1


# Record test retry
def record_retry(test_name):

    # Increase retry counter
    flaky_data["retried_tests"] += 1

    # Add test to flaky list if not already exists
    if test_name not in flaky_data["flaky_tests"]:
        flaky_data["flaky_tests"].append(test_name)

    # Initialize retry counter for test if needed
    if test_name not in flaky_data["retry_count"]:
        flaky_data["retry_count"][test_name] = 0

    # Increase retry count for specific test
    flaky_data["retry_count"][test_name] += 1


# Save flaky analytics report to JSON file
def save_report():

    # Get report path from environment variable or use default local path
    report_path = os.environ.get(
        "FLAKY_REPORT_FILE",
        "flaky-reports/flaky_report.json"
    )

    # Get folder path from report file path
    report_folder = os.path.dirname(report_path)

    # Create report folder if it does not exist
    if report_folder and not os.path.exists(report_folder):
        os.makedirs(report_folder)

    # Write flaky report into JSON file
    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(flaky_data, file, indent=4)