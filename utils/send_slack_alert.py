import os
import requests

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")
BUILD_NUMBER = os.getenv("BUILD_NUMBER", "N/A")

S3_BASE = "https://qa-automation-reports-bucket-sefi.s3.eu-central-1.amazonaws.com"
AGG_FILE = "flaky-reports/aggregated-latest.json"


def load_data():
    try:
        res = requests.get(f"{S3_BASE}/{AGG_FILE}")
        return res.json()
    except:
        return {}


def format_top_flaky(top_flaky):
    if not top_flaky:
        return "No flaky tests 🎉"

    lines = []
    for i, test in enumerate(top_flaky, start=1):
        lines.append(f"{i}. {test['test_name']} ({test['retry_count']} retries)")

    return "\n".join(lines)


def send_slack():

    data = load_data()

    total = data.get("total_tests", 0)
    passed = data.get("passed_tests", 0)
    failed = data.get("failed_tests", 0)
    pass_rate = data.get("pass_rate", 0)

    flaky = data.get("total_flaky_tests", 0)
    flaky_rate = data.get("flaky_rate", 0)

    top_flaky = data.get("top_flaky_tests", [])

    # צבע
    if failed > 0:
        color = "#ff0000"
    elif flaky > 0:
        color = "#ffcc00"
    else:
        color = "#36a64f"

    message = {
        "attachments": [
            {
                "color": color,
                "title": f"QA Automation Build #{BUILD_NUMBER}",
                "text": f"*Top Flaky Tests:*\n{format_top_flaky(top_flaky)}",
                "fields": [
                    {"title": "Total", "value": str(total), "short": True},
                    {"title": "Passed", "value": str(passed), "short": True},
                    {"title": "Failed", "value": str(failed), "short": True},
                    {"title": "Pass Rate", "value": f"{pass_rate}%", "short": True},
                    {"title": "Flaky", "value": str(flaky), "short": True},
                    {"title": "Flaky Rate", "value": f"{flaky_rate}%", "short": True},
                ],
                "actions": [
                    {
                        "type": "button",
                        "text": "Allure Report",
                        "url": f"{S3_BASE}/allure-latest/index.html"
                    },
                    {
                        "type": "button",
                        "text": "Flaky Dashboard",
                        "url": f"{S3_BASE}/{AGG_FILE}"
                    }
                ]
            }
        ]
    }

    requests.post(SLACK_WEBHOOK, json=message)


if __name__ == "__main__":
    send_slack()