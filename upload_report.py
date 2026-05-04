import os
from datetime import datetime


BUCKET_NAME = "qa-automation-reports-bucket-sefi"


def upload_html_report_to_s3():
    report_path = "/app/report.html"

    if not os.path.exists(report_path):
        print("report.html was not found. Skipping S3 upload.")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    s3_report_name = f"report-{timestamp}.html"

    upload_command = (
        f"aws s3 cp {report_path} "
        f"s3://{BUCKET_NAME}/{s3_report_name}"
    )

    print(f"Uploading report to S3: s3://{BUCKET_NAME}/{s3_report_name}")

    exit_code = os.system(upload_command)

    if exit_code != 0:
        raise Exception("Failed to upload report to S3")

    print("Report uploaded to S3 successfully")


if __name__ == "__main__":
    upload_html_report_to_s3()