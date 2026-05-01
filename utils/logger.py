# Python built-in logging library
import logging

# OS library for folder handling
import os

# Rotating file handler for log file size control
from logging.handlers import RotatingFileHandler


# =========================================================
# Create logs folder if it does not exist
# יצירת תיקיית logs אם אינה קיימת
# =========================================================
if not os.path.exists("logs"):
    os.makedirs("logs")


# =========================================================
# Create logger object
# יצירת אובייקט לוגר מרכזי
# =========================================================
logger = logging.getLogger("automation_logger")

# Set global logging level
# קביעת רמת לוג כללית
logger.setLevel(logging.DEBUG)


# =========================================================
# Prevent duplicate handlers
# מניעת יצירת handlers כפולים
# =========================================================
if not logger.handlers:

    # =====================================================
    # File handler with rotation
    # Handler לקובץ עם הגבלת גודל וסיבוב קבצים
    # =====================================================
    file_handler = RotatingFileHandler(
        "logs/test_execution.log",
        maxBytes=2_000_000,      # 2MB max file size
        backupCount=3,           # keep 3 backup files
        encoding="utf-8"
    )

    # Set file logging level
    file_handler.setLevel(logging.DEBUG)


    # =====================================================
    # Console handler
    # Handler להצגת לוגים בטרמינל
    # =====================================================
    console_handler = logging.StreamHandler()

    # Set console logging level
    console_handler.setLevel(logging.INFO)


    # =====================================================
    # Log format
    # פורמט אחיד ללוגים
    # =====================================================
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )


    # Apply formatter to handlers
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)


    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)