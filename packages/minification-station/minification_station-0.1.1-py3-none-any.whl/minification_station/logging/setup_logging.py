from datetime import datetime  # Import datetime to format the date
import logging
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler  # Import TimedRotatingFileHandler
from pathlib import Path

from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

LOG_LEVEL = logging.INFO


def setup_logging(log_file: Path, log_level: int = logging.INFO) -> None:
    """Sets up logging configuration."""
    install_rich_traceback(max_frames=2, suppress=["sqlalchemy", "sqlalchemy.orm", "mysql", "mysql-connector-python"])

    # Get the current date and format it
    current_date = datetime.now().strftime("%Y-%m-%d")
    # Prepend the date to the log file name
    log_file_with_date = Path("logs") / f"{current_date}_{log_file.name}"
    error_log_file_with_date = Path("logs") / f"{current_date}_error.log"  # New error log file

    dictConfig(
        {
            "version": 1,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "generic": {
                    "format": "%(asctime)s %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "class": "logging.Formatter",
                },
                "file_formatter": {  # New formatter for file logging
                    "format": "%(asctime)s - %(levelname)s - %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "handlers": {
                "fileHandler": {
                    "class": "logging.handlers.TimedRotatingFileHandler",  # Use TimedRotatingFileHandler
                    "filename": log_file_with_date,  # Use the new filename with date
                    "formatter": "file_formatter",  # Use the new formatter
                    "level": "DEBUG",  # Log everything to file
                    "when": "midnight",  # Create a new log file every day at midnight
                    "backupCount": 7,  # Keep 7 days of log files
                    "encoding": "utf-8",  # Optional: specify encoding
                },
                "errorFileHandler": {  # New handler for error logging
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "filename": error_log_file_with_date,  # Error log file
                    "formatter": "file_formatter",
                    "level": "ERROR",  # Log only errors
                    "when": "midnight",
                    "backupCount": 7,
                    "encoding": "utf-8",
                },
                "console": {
                    "class": "rich.logging.RichHandler",
                    "formatter": "generic",
                    "level": log_level,  # Dynamic log level
                    "rich_tracebacks": True,
                },
            },
            "root": {"level": log_level, "handlers": ["fileHandler", "errorFileHandler", "console"]},
        },
    )
