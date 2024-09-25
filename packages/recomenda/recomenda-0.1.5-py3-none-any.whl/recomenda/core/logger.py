import logging
from datetime import datetime
import pytz
from typing import Optional
import os

class Logger(logging.Logger):
    def __init__(
        self,
        name: str = "RecommenderLogger",
        timezone: str = 'America/Sao_Paulo',
        level: int = logging.INFO,
        log_format: str = '%(asctime)s - %(levelname)s - %(message)s',
        output: str = 'console',
        log_file: Optional[str] = None
    ):
        """
        Initialize the Logger class, inheriting from logging.Logger.

        Args:
            name (str): The name of the logger.
            timezone (str): The timezone for the log timestamps.
            level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
            log_format (str): The format string for log messages.
            output (str): Output type ('console', 'file'). If 'file', a file handler is added.
            log_file (Optional[str]): The path to the log file. Required if output is 'file'.
        """
        super().__init__(name, level)
        self.timezone = pytz.timezone(timezone)

        # Create formatter
        formatter = self.ConfigurableFormatter(fmt=log_format, timezone=timezone)

        # Create handlers based on output type
        if output == 'console':
            handler = logging.StreamHandler()
        elif output == 'file':
            if log_file is None:
                raise ValueError("log_file must be provided when output is 'file'")
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            handler = logging.FileHandler(log_file)
        else:
            raise ValueError("Output must be either 'console' or 'file'.")

        handler.setFormatter(formatter)

        # Add handler to logger if not already added
        if not self.hasHandlers():
            self.addHandler(handler)

    class ConfigurableFormatter(logging.Formatter):
        def __init__(self, fmt: str, timezone: str = 'UTC'):
            super().__init__(fmt)
            self.timezone = pytz.timezone(timezone)

        def formatTime(self, record, datefmt: Optional[str] = None) -> str:
            dt = datetime.fromtimestamp(record.created, tz=self.timezone)
            if datefmt:
                return dt.strftime(datefmt)
            return dt.isoformat()

# Usage example:
# Creating a logger instance with default settings
logger = Logger()

# Now you can use it directly
# logger.info("This is an info message.")

# Creating a file logger with custom settings
# file_logger = Logger(output='file', level=logging.DEBUG)
# file_logger.debug("This is a debug message written to the file.")
