import os
from datetime import datetime

BUCKET_NAME = "qa-automation-reports-bucket-sefi"


def run_cmd(cmd):
    print(f"Running: {cmd}")
    if os.system(cmd) != 0:
        raise Exception(f"Command failed: {cmd}")


def upload_html_report():
    report_path = "/app/report.html"

    if not os.path.exists(report_path):
        print("report.html not found - skipping upload")
        return None

    report_file = os.getenv("REPORT_FILE")

    if report_file:
        s3_name = report_file
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        s3_name = f"report-{timestamp}.html"

    print(f"Uploading report: {s3_name}")

    run_cmd(f"aws s3 cp {report_path} s3://{BUCKET_NAME}/{s3_name}")
    run_cmd(f"aws s3 cp {report_path} s3://{BUCKET_NAME}/latest.html")

    return s3_name


def upload_allure_report():
    allure_path = "/app/allure-report"

    if not os.path.exists(allure_path):
        print("Allure report not found - skipping upload")
        return

    print("Uploading Allure report...")

    run_cmd(
        f"aws s3 cp {allure_path} "
        f"s3://{BUCKET_NAME}/allure-latest/ "
        f"--recursive"
    )


def upload_flaky_report():
    flaky_report_path = "/app/flaky-reports/flaky_report.json"

    if not os.path.exists(flaky_report_path):
        print("flaky_report.json not found - skipping flaky report upload")
        return

    report_file = os.getenv("REPORT_FILE")

    if report_file:
        build_id = report_file.replace("report-", "").replace(".html", "")
        flaky_report_name = f"flaky-report-{build_id}.json"
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        flaky_report_name = f"flaky-report-{timestamp}.json"

    print(f"Uploading flaky report: {flaky_report_name}")

    run_cmd(
        f"aws s3 cp {flaky_report_path} "
        f"s3://{BUCKET_NAME}/flaky-reports/{flaky_report_name}"
    )

    run_cmd(
        f"aws s3 cp {flaky_report_path} "
        f"s3://{BUCKET_NAME}/flaky-reports/latest.json"
    )


def main():
    upload_html_report()
    upload_allure_report()
    upload_flaky_report()
    print("All uploads completed successfully")


if __name__ == "__main__":
    main()