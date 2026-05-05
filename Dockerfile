# Use official Microsoft Playwright image with Python support
FROM mcr.microsoft.com/playwright/python:v1.59.0-jammy

# Set working directory inside container
WORKDIR /app

# Copy only requirements first to improve Docker cache
COPY requirements.txt .

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python dependencies
RUN pip install -r requirements.txt

# Install AWS CLI for uploading reports to S3
RUN pip install awscli

# Install Java + Allure CLI
RUN apt-get update && \
    apt-get install -y wget unzip openjdk-11-jre && \
    wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip && \
    unzip allure-2.29.0.zip -d /opt/ && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure && \
    rm allure-2.29.0.zip && \
    apt-get clean

# Copy full project into container
COPY . .

# Default command:
# 1. Run all real tests in parallel (exclude demo)
# 2. Save pytest exit code
# 3. Generate Flaky dashboard
# 4. Generate Allure report (even on failure)
# 5. Upload reports to S3
# 6. Exit with original pytest result
CMD ["bash", "-c", "\
pytest -n 3 -m \"not demo\" --env=dev --reruns 2 --reruns-delay 2; \
TEST_EXIT_CODE=$?; \
python utils/flaky_dashboard.py; \
allure generate allure-results -o allure-report --clean || true; \
python upload_report.py; \
exit $TEST_EXIT_CODE \
"]