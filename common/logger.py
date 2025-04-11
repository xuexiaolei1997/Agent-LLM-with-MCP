# This module provides a logger for the application.
# It uses the logging library to create a logger that can be used throughout the application.
# The logger is configured to log messages to a file and to the console.
# The log level can be set to DEBUG, INFO, WARNING, ERROR, or CRITICAL.

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get the log level from environment variables, default to INFO if not set
log_level = os.getenv("LOG_LEVEL", "INFO").upper()
if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    raise ValueError(f"Invalid log level: {log_level}. Must be one of DEBUG, INFO, WARNING, ERROR, CRITICAL.")

def setup_logger():
    """
    Sets up the logger for the application.
    The logger will log messages to both a file and the console.
    """
    # Create a directory for logs if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create a unique log file name based on the current date and time
    log_file = log_dir / f"{datetime.now().strftime('%Y%m%d')}.log"

    # Create a logger
    logger = logging.getLogger("agent_logger")
    logger.setLevel(getattr(logging, log_level))

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(getattr(logging, log_level))

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, log_level))

    # Create formatter and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Initialize the logger
logger = setup_logger()
logger.info("Logger is set up and ready to use.")
