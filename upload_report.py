import os
from datetime import datetime

BUCKET_NAME = "qa-automation-reports-bucket-sefi"

def run_command(cmd):
    print(f"Running: {cmd}")
    if os.system(cmd) != 0:
        raise Exception(f"Command failed: {cmd}")

def upload_html_report():
    report_path = "/app/report.html"

    if not os.path.exists(report_path):
        print("report.html not found, skipping HTML upload")
        return None

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    report_name = f"report-{timestamp}.html"

    run_command(f"aws s3 cp {report_path} s3://{BUCKET_NAME}/{report_name}")
    run_command(f"aws s3 cp {report_path} s3://{BUCKET_NAME}/latest.html")

    return report_name

def upload_allure_report():
    allure_dir = "/app/allure-report"

    if not os.path.exists(allure_dir):
        print("Allure report not found, skipping")
        return

    # מחיקת הקודם
    run_command(f"aws s3 rm s3://{BUCKET_NAME}/allure-latest/ --recursive")

    # העלאה חדשה
    run_command(f"aws s3 cp {allure_dir} s3://{BUCKET_NAME}/allure-latest/ --recursive")

def send_slack_notification(report_name):
    slack_webhook = os.getenv("SLACK_WEBHOOK_URL")

    if not slack_webhook:
        print("No Slack webhook configured")
        return

    allure_url = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/allure-latest/index.html"
    html_url = f"https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/{report_name}"

    message = f"""
QA Results:
Report: {html_url}
Allure: {allure_url}
"""

    payload = f"""curl -X POST -H 'Content-type: application/json' \
--data '{{"text":"{message}"}}' {slack_webhook}"""

    run_command(payload)

if __name__ == "__main__":
    report_name = upload_html_report()
    upload_allure_report()

    if report_name:
        send_slack_notification(report_name)