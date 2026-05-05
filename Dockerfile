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

# Install Allure CLI
RUN apt-get update && \
    apt-get install -y wget unzip && \
    wget https://github.com/allure-framework/allure2/releases/download/2.29.0/allure-2.29.0.zip && \
    unzip allure-2.29.0.zip -d /opt/ && \
    ln -s /opt/allure-2.29.0/bin/allure /usr/bin/allure && \
    rm allure-2.29.0.zip && \
    apt-get clean

# Copy full project into container
COPY . .

# Default command:
# 1. Run regression tests and save pytest exit code
# 2. Generate Allure report even if tests fail
# 3. Upload HTML + Allure reports to S3
# 4. Exit with original pytest exit code so Jenkins can still fail correctly
CMD ["bash", "-c", "pytest -m 'regression and not demo' --env=dev; TEST_EXIT_CODE=$?; allure generate allure-results -o allure-report --clean; python upload_report.py; exit $TEST_EXIT_CODE"]