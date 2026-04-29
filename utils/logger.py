# Python built-in logging library
import logging

# OS library for folder handling
import os


# Create logs folder if it does not exist
if not os.path.exists("logs"):
    os.makedirs("logs")


# Create logger object
logger = logging.getLogger("automation_logger")

# Set logger level
logger.setLevel(logging.INFO)

# Prevent duplicate logs
if not logger.handlers:

    # File handler for saving logs into file
    file_handler = logging.FileHandler(
        "logs/test_execution.log",
        mode="a",
        encoding="utf-8"
    )

    # Console handler for terminal output
    console_handler = logging.StreamHandler()

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    # Apply format to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)