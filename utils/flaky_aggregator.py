import json
import os
from collections import defaultdict
from datetime import datetime

BUCKET_NAME = "qa-automation-reports-bucket-sefi"
LOCAL_DIR = "flaky-aggregated"


def run_cmd(cmd):
    print(f"Running: {cmd}")
    exit_code = os.system(cmd)
    if exit_code != 0:
        raise Exception(f"Command failed: {cmd}")


def extract_build_number():
    return os.getenv("BUILD_NUMBER", "unknown")


def download_report(build_number, suite):
    s3_path = f"s3://{BUCKET_NAME}/flaky-reports/flaky-report-{build_number}-{suite}.json"
    local_path = f"{LOCAL_DIR}/{suite}.json"

    cmd = f"aws s3 cp {s3_path} {local_path}"
    if os.system(cmd) != 0:
        print(f"Skipping missing report: {suite}")
        return None

    return local_path


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def aggregate(build_number):

    suites = ["api", "ui", "db"]

    total_tests = 0
    total_flaky = 0
    total_retried = 0

    passed_tests = 0
    failed_tests = 0

    retry_counter = defaultdict(int)

    aggregated = {
        "build_number": build_number,
        "generated_at": datetime.utcnow().isoformat(),
        "suites": {}
    }

    for suite in suites:
        path = download_report(build_number, suite)

        if not path:
            continue

        data = load_json(path)

        suite_total = data.get("total_tests", 0)
        suite_flaky = data.get("total_flaky_tests", 0)
        suite_retried = data.get("total_retried_tests", 0)

        total_tests += suite_total
        total_flaky += suite_flaky
        total_retried += suite_retried

        # נחשב passed/failed (בקירוב)
        suite_failed = suite_retried  # כשלו לפחות פעם
        suite_passed = suite_total - suite_failed

        passed_tests += suite_passed
        failed_tests += suite_failed

        # ספירת flaky לפי טסט
        for test in data.get("flaky_tests", []):
            retry_counter[test["test_name"]] += test.get("retry_count", 1)

        aggregated["suites"][suite] = {
            "total_tests": suite_total,
            "flaky_tests": suite_flaky,
            "retried_tests": suite_retried
        }

    # 🔥 Top Flaky Tests
    top_flaky = sorted(
        [{"test_name": k, "retry_count": v} for k, v in retry_counter.items()],
        key=lambda x: x["retry_count"],
        reverse=True
    )[:5]

    # חישובים כלליים
    flaky_rate = round((total_flaky / total_tests) * 100, 2) if total_tests else 0
    pass_rate = round((passed_tests / total_tests) * 100, 2) if total_tests else 0

    aggregated.update({
        "total_tests": total_tests,
        "passed_tests": passed_tests,
        "failed_tests": failed_tests,
        "pass_rate": pass_rate,
        "total_flaky_tests": total_flaky,
        "flaky_rate": flaky_rate,
        "top_flaky_tests": top_flaky
    })

    return aggregated


def save_and_upload(build_number, data):

    os.makedirs(LOCAL_DIR, exist_ok=True)

    filename = f"{LOCAL_DIR}/flaky-report-{build_number}-aggregated.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    print(json.dumps(data, indent=4))

    run_cmd(f"aws s3 cp {filename} s3://{BUCKET_NAME}/flaky-reports/flaky-report-{build_number}-aggregated.json")
    run_cmd(f"aws s3 cp {filename} s3://{BUCKET_NAME}/flaky-reports/aggregated-latest.json")


if __name__ == "__main__":
    build = extract_build_number()
    result = aggregate(build)
    save_and_upload(build, result)