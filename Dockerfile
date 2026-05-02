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

# Copy project files after dependencies
COPY . .

# Default command for regression execution
CMD ["python", "-m", "pytest", "-m", "regression and not demo", "--env=dev"]