import os
from datetime import datetime

BUCKET_NAME = "qa-automation-reports-bucket-sefi"


def upload_html_report_to_s3():
    report_path = "/app/report.html"
    allure_report_path = "/app/allure-report"

    if not os.path.exists(report_path):
        print("report.html was not found. Skipping HTML report upload.")
    else:
        report_file = os.getenv("REPORT_FILE")

        if report_file:
            s3_report_name = report_file
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
            s3_report_name = f"report-{timestamp}.html"

        upload_main = f"aws s3 cp {report_path} s3://{BUCKET_NAME}/{s3_report_name}"
        upload_latest = f"aws s3 cp {report_path} s3://{BUCKET_NAME}/latest.html"

        print(f"Uploading HTML report: s3://{BUCKET_NAME}/{s3_report_name}")

        if os.system(upload_main) != 0:
            raise Exception("Failed to upload main HTML report")

        print("Uploading latest.html")

        if os.system(upload_latest) != 0:
            raise Exception("Failed to upload latest HTML report")

        print("HTML report + latest.html uploaded successfully")

    if os.path.exists(allure_report_path):
        allure_folder = os.getenv("ALLURE_REPORT_FOLDER", "allure-latest")

        upload_allure = (
            f"aws s3 sync {allure_report_path} "
            f"s3://{BUCKET_NAME}/{allure_folder}/ --delete"
        )

        print(f"Uploading Allure report: s3://{BUCKET_NAME}/{allure_folder}/")

        if os.system(upload_allure) != 0:
            raise Exception("Failed to upload Allure report")

        print("Allure report uploaded successfully")
        print(f"Allure URL: https://{BUCKET_NAME}.s3.eu-central-1.amazonaws.com/{allure_folder}/index.html")
    else:
        print("allure-report folder was not found. Skipping Allure upload.")


if __name__ == "__main__":
    upload_html_report_to_s3()