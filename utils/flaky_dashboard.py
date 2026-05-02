# Import JSON library for reading and writing reports
import json

# Import OS library for file and folder handling
import os

# Import UUID library for unique Allure result IDs
import uuid

# Import time library for Allure timestamps
import time


# Define flaky report folders created by Jenkins parallel suites
FLAKY_REPORT_FOLDERS = {
    "API": "flaky-reports-api/flaky_report.json",
    "UI + FullStack": "flaky-reports-ui/flaky_report.json",
    "DB": "flaky-reports-db/flaky_report.json",
    "Auth": "flaky-reports-auth/flaky_report.json",
}


# Define Allure output folder for dashboard result
ALLURE_OUTPUT_FOLDER = "allure-results-flaky"


# Read flaky report from file
def read_flaky_report(file_path):

    # Return empty report if file does not exist
    if not os.path.exists(file_path):
        return {
            "total_tests": 0,
            "retried_tests": 0,
            "flaky_tests": [],
            "retry_count": {}
        }

    # Open and load flaky report JSON
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Build aggregated flaky dashboard data
def build_dashboard_data():

    # Create dashboard structure
    dashboard = {
        "total_tests": 0,
        "total_retried_tests": 0,
        "suites": {},
        "flaky_tests": []
    }

    # Read each suite flaky report
    for suite_name, report_path in FLAKY_REPORT_FOLDERS.items():

        # Load suite report
        report = read_flaky_report(report_path)

        # Add suite data to dashboard
        dashboard["suites"][suite_name] = report

        # Add suite totals
        dashboard["total_tests"] += report.get("total_tests", 0)
        dashboard["total_retried_tests"] += report.get("retried_tests", 0)

        # Add flaky test details
        for test_name in report.get("flaky_tests", []):
            dashboard["flaky_tests"].append({
                "suite": suite_name,
                "test_name": test_name,
                "retry_count": report.get("retry_count", {}).get(test_name, 0)
            })

    # Return final dashboard data
    return dashboard


# Create readable text summary for Allure attachment
def create_text_summary(dashboard):

    # Build summary lines
    lines = [
        "Flaky Test Analytics Dashboard",
        "================================",
        "",
        f"Total executed tests: {dashboard['total_tests']}",
        f"Total retried tests: {dashboard['total_retried_tests']}",
        f"Total flaky tests: {len(dashboard['flaky_tests'])}",
        "",
        "Suite Breakdown:",
        "----------------"
    ]

    # Add each suite summary
    for suite_name, report in dashboard["suites"].items():
        lines.append(
            f"{suite_name}: total={report.get('total_tests', 0)}, "
            f"retried={report.get('retried_tests', 0)}, "
            f"flaky={len(report.get('flaky_tests', []))}"
        )

    # Add flaky test list
    lines.append("")
    lines.append("Flaky Tests:")
    lines.append("------------")

    # Add no flaky message if empty
    if not dashboard["flaky_tests"]:
        lines.append("No flaky tests detected.")

    # Add flaky test details
    for flaky_test in dashboard["flaky_tests"]:
        lines.append(
            f"{flaky_test['suite']} | {flaky_test['test_name']} | "
            f"retries={flaky_test['retry_count']}"
        )

    # Return text content
    return "\n".join(lines)


# Write Allure compatible result file
def write_allure_dashboard(dashboard):

    # Create Allure output folder if needed
    os.makedirs(ALLURE_OUTPUT_FOLDER, exist_ok=True)

    # Create unique IDs
    result_uuid = str(uuid.uuid4())
    summary_json_name = f"{result_uuid}-flaky-summary.json"
    summary_text_name = f"{result_uuid}-flaky-summary.txt"
    result_file_name = f"{result_uuid}-result.json"

    # Write JSON attachment
    with open(os.path.join(ALLURE_OUTPUT_FOLDER, summary_json_name), "w", encoding="utf-8") as file:
        json.dump(dashboard, file, indent=4)

    # Write text attachment
    with open(os.path.join(ALLURE_OUTPUT_FOLDER, summary_text_name), "w", encoding="utf-8") as file:
        file.write(create_text_summary(dashboard))

    # Create Allure result body
    allure_result = {
        "uuid": result_uuid,
        "historyId": "flaky-analytics-dashboard",
        "name": "Flaky Analytics Dashboard",
        "fullName": "Flaky Analytics Dashboard",
        "status": "passed",
        "stage": "finished",
        "description": "Aggregated flaky test analytics generated from all parallel Docker suites.",
        "labels": [
            {"name": "suite", "value": "Flaky Analytics"},
            {"name": "feature", "value": "Flaky Test Analytics"},
            {"name": "story", "value": "Retry and Stability Dashboard"}
        ],
        "attachments": [
            {
                "name": "Flaky Summary",
                "source": summary_text_name,
                "type": "text/plain"
            },
            {
                "name": "Flaky Report JSON",
                "source": summary_json_name,
                "type": "application/json"
            }
        ],
        "start": int(time.time() * 1000),
        "stop": int(time.time() * 1000)
    }

    # Write Allure result file
    with open(os.path.join(ALLURE_OUTPUT_FOLDER, result_file_name), "w", encoding="utf-8") as file:
        json.dump(allure_result, file, indent=4)


# Main execution
if __name__ == "__main__":

    # Build dashboard data
    dashboard_data = build_dashboard_data()

    # Write dashboard into Allure result format
    write_allure_dashboard(dashboard_data)