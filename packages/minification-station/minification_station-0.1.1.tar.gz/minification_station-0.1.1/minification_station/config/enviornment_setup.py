from datetime import datetime
import logging
import os
from pathlib import Path
import sys

from minification_station.logging.setup_logging import setup_logging

LOG_FILE = "main.log"
LOG_PATH = Path("logs")
LOG_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH = LOG_PATH / LOG_FILE
OUTPUT_PATH = Path("output")

ISO_DATE_FORMAT = "%y%m%dT%H-%M"


def ensure_directory_exists(path: Path) -> None:
    """Ensure that the directory for the given path exists; create it if it does not."""
    if not path.exists():
        logging.info(f"Directory {path.resolve()} does not exist. Creating it.")
        path.mkdir(parents=True, exist_ok=True)
        logging.info(f"Directory {path.resolve()} created.")

def get_current_date_formatted(_format: str) -> str:
    """Return the current date formatted according to the given format string."""
    return datetime.now().strftime(_format)


def initialize_application() -> None:
    """Initialize application by setting up environment, logging and ensuring directory structure."""
    log_level = logging.INFO

    setup_logging(LOG_PATH, log_level)
    logging.debug("Initializing application...")
    logging.debug("Application initialized.")
    ensure_directory_exists(OUTPUT_PATH)

def validate_directory(directory: str) -> None:
    """Validate that the provided directory exists and is a directory."""
    if not os.path.isdir(directory):
        logging.error(f"The directory '{directory}' is not valid.")
        msg = f"The directory '{directory}' is not valid."
        raise ValueError(msg)

current_date: str = get_current_date_formatted(ISO_DATE_FORMAT)
