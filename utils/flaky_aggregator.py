import json
import os
from datetime import datetime


BUCKET_NAME = "qa-automation-reports-bucket-sefi"
LOCAL_OUTPUT_DIR = "flaky-aggregated"


def run_cmd(cmd):
    print(f"Running: {cmd}")
    exit_code = os.system(cmd)

    if exit_code != 0:
        raise Exception(f"Command failed: {cmd}")


def extract_build_number():
    build_number = os.getenv("BUILD_NUMBER")

    if build_number:
        return build_number

    report_file = os.getenv("REPORT_FILE")

    if report_file:
        return (
            report_file
            .replace("report-", "")
            .replace("-api.html", "")
            .replace("-ui.html", "")
            .replace("-db.html", "")
            .replace(".html", "")
        )

    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def download_flaky_report(build_number, suite_name):
    s3_key = f"flaky-reports/flaky-report-{build_number}-{suite_name}.json"
    local_file = os.path.join(LOCAL_OUTPUT_DIR, f"{suite_name}.json")

    cmd = (
        f"aws s3 cp "
        f"s3://{BUCKET_NAME}/{s3_key} "
        f"{local_file}"
    )

    exit_code = os.system(cmd)

    if exit_code != 0:
        print(f"Flaky report not found for suite: {suite_name}")
        return None

    return local_file


def read_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def aggregate_reports(report_files):
    aggregated = {
        "total_tests": 0,
        "total_retried_tests": 0,
        "total_flaky_tests": 0,
        "suites": {},
        "flaky_tests": [],
        "generated_at": datetime.now().isoformat()
    }

    for suite_name, file_path in report_files.items():
        if not file_path:
            continue

        report = read_json_file(file_path)

        total_tests = report.get("total_tests", 0)
        retried_tests = report.get("retried_tests", 0)
        flaky_tests = report.get("flaky_tests", [])
        retry_count = report.get("retry_count", {})

        aggregated["total_tests"] += total_tests
        aggregated["total_retried_tests"] += retried_tests

        aggregated["suites"][suite_name] = {
            "total_tests": total_tests,
            "retried_tests": retried_tests,
            "flaky_tests": flaky_tests,
            "retry_count": retry_count
        }

        for test_name in flaky_tests:
            aggregated["flaky_tests"].append({
                "suite": suite_name,
                "test_name": test_name,
                "retry_count": retry_count.get(test_name, 0)
            })

    aggregated["total_flaky_tests"] = len(aggregated["flaky_tests"])

    if aggregated["total_tests"] > 0:
        aggregated["flaky_rate"] = round(
            (aggregated["total_flaky_tests"] / aggregated["total_tests"]) * 100,
            2
        )
    else:
        aggregated["flaky_rate"] = 0

    return aggregated


def upload_aggregated_report(build_number, aggregated_file):
    run_cmd(
        f"aws s3 cp {aggregated_file} "
        f"s3://{BUCKET_NAME}/flaky-reports/flaky-report-{build_number}-aggregated.json"
    )

    run_cmd(
        f"aws s3 cp {aggregated_file} "
        f"s3://{BUCKET_NAME}/flaky-reports/aggregated-latest.json"
    )


def main():
    os.makedirs(LOCAL_OUTPUT_DIR, exist_ok=True)

    build_number = extract_build_number()

    print(f"Aggregating flaky reports for build: {build_number}")

    suites = ["api", "ui", "db"]

    report_files = {}

    for suite_name in suites:
        report_files[suite_name] = download_flaky_report(build_number, suite_name)

    aggregated = aggregate_reports(report_files)

    output_file = os.path.join(
        LOCAL_OUTPUT_DIR,
        f"flaky-report-{build_number}-aggregated.json"
    )

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(aggregated, file, indent=4)

    print("Aggregated flaky report created successfully")
    print(json.dumps(aggregated, indent=4))

    upload_aggregated_report(build_number, output_file)

    print("Aggregated flaky report uploaded successfully")


if __name__ == "__main__":
    main()