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
# 1. Run regression tests
# 2. Generate Allure report
# 3. Upload HTML + Allure reports to S3
CMD ["bash", "-c", "pytest -m 'regression and not demo' --env=dev && allure generate allure-results -o allure-report --clean && python upload_report.py"]