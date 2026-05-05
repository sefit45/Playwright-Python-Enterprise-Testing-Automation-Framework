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
        print("report.html not found, skipping...")
        return

    report_file = os.getenv("REPORT_FILE")

    if report_file:
        s3_report_name = report_file
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        s3_report_name = f"report-{timestamp}.html"

    # Upload main report
    run_command(
        f"aws s3 cp {report_path} s3://{BUCKET_NAME}/{s3_report_name} --acl public-read"
    )

    # Upload latest.html
    run_command(
        f"aws s3 cp {report_path} s3://{BUCKET_NAME}/latest.html --acl public-read"
    )


def upload_allure_report():
    allure_dir = "/app/allure-report"

    if not os.path.exists(allure_dir):
        print("No allure-report directory found, skipping...")
        return

    # Upload full folder
    run_command(
        f"aws s3 cp {allure_dir} s3://{BUCKET_NAME}/allure-latest/ --recursive --acl public-read"
    )


if __name__ == "__main__":
    print("Uploading reports to S3...")

    upload_html_report()
    upload_allure_report()

    print("All uploads completed successfully")