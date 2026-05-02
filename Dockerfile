# Use official Python image as base image
FROM python:3.14-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required by Playwright browsers
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file into container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers and required OS dependencies
RUN playwright install --with-deps

# Copy full project into container
COPY . .

# Default command for running regression tests
CMD ["python", "-m", "pytest", "-m", "regression and not demo", "--env=dev"]