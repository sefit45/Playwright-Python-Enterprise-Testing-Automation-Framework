import os
from datetime import datetime

BUCKET_NAME = "qa-automation-reports-bucket-sefi"

def upload_html_report_to_s3():
    report_path = "/app/report.html"

    if not os.path.exists(report_path):
        print("report.html was not found. Skipping S3 upload.")
        return

    report_file = os.getenv("REPORT_FILE")

    if report_file:
        s3_report_name = report_file
    else:
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        s3_report_name = f"report-{timestamp}.html"

    # 🎯 דוח לפי Build
    upload_main = f"aws s3 cp {report_path} s3://{BUCKET_NAME}/{s3_report_name}"

    # 🎯 latest.html (תמיד האחרון)
    upload_latest = f"aws s3 cp {report_path} s3://{BUCKET_NAME}/latest.html"

    print(f"Uploading report: {s3_report_name}")

    if os.system(upload_main) != 0:
        raise Exception("Failed to upload main report")

    print("Uploading latest.html")

    if os.system(upload_latest) != 0:
        raise Exception("Failed to upload latest report")

    print("Report + latest.html uploaded successfully")

if __name__ == "__main__":
    upload_html_report_to_s3()