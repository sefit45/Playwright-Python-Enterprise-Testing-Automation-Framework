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
# 1. Use PYTEST_MARKER when provided by Jenkins/ECS
# 2. Run tests in parallel inside the container
# 3. Exclude demo tests
# 4. Save pytest exit code
# 5. Generate Flaky dashboard
# 6. Generate Allure report
# 7. Upload reports to S3
# 8. Exit with original pytest result
CMD ["bash", "-c", "\
if [ -z \"$PYTEST_MARKER\" ]; then \
  PYTEST_MARKER='not demo'; \
else \
  PYTEST_MARKER=\"($PYTEST_MARKER) and not demo\"; \
fi; \
echo \"Running pytest marker: $PYTEST_MARKER\"; \
pytest -n 3 -m \"$PYTEST_MARKER\" --env=dev --reruns 2 --reruns-delay 2; \
TEST_EXIT_CODE=$?; \
python utils/flaky_dashboard.py; \
allure generate allure-results -o allure-report --clean || true; \
python upload_report.py; \
exit $TEST_EXIT_CODE \
"]