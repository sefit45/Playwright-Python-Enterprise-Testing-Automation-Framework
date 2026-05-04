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

# Copy full project into container
COPY . .

# Default command:
# 1. Run regression tests
# 2. Upload HTML report to S3 only if tests passed
CMD ["bash", "-c", "python -m pytest -m 'regression and not demo' --env=dev && python upload_report.py"]