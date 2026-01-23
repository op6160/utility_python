"""
Logger Utility Library

Provides formatters and pre-configured logger instances for console output and file logging.

Available Objects:
    - log_msg: Basic console output logger (includes timestamp).
    - debug: Debug logger (console output + saves to logs/debug.log).
    - MSGFormatter: Class for creating custom loggers.
"""
import sys
import os
from .module.logger_lib.formatter import MessageFormatter, make_print_formatter
from .time_lib import detail as __detailtime
from .py_lib import get_python_filename as __get_python_filename
from .py_lib import get_python_codeline as __get_python_codeline
MSGFormatter = MessageFormatter

__all__ = [
    "MSGFormatter",
    "log_msg",
    "debug",
    "make_print_formatter",
]

class DynamicLogger:
    """
    A wrapper class to generate headers dynamically at runtime.
    """
    def __init__(self, formatter, header_factory):
        self.formatter = formatter
        self.header_factory = header_factory

    def __call__(self, msg):
        # Generate header at the moment of logging
        header = self.header_factory()
        # Pass the combined string to the underlying formatter
        # We assume the underlying formatter is initialized with an empty header
        self.formatter(f"{header}{msg}")

    def override(self, **kwargs):
        # Allow creating new instances with overrides (like debug logger)
        return DynamicLogger(self.formatter.override(**kwargs), self.header_factory)

# basic logger(print only)
# Initialize base formatter with empty header, handle header dynamically
log_msg = DynamicLogger(
    MessageFormatter(header=""), 
    lambda: f"[{__detailtime}] "  # This lambda runs every time log_msg() is called
)

# debug logger (with file saving)
debug = log_msg.override(file_path="logs/debug.log")
# For debug, we might want a fixed header like [DEBUG], or dynamic time. 
# Assuming we want time + [DEBUG]:
debug.header_factory = lambda: f"[{__detailtime}] [DEBUG] "

# function usage example
warning = DynamicLogger(
    make_print_formatter(header=""),
    # depth=2 is needed because: warning() -> DynamicLogger.__call__() -> get_python_filename()
    lambda: f"[{__get_python_filename(2)}: {__get_python_codeline(2)}lines] Warning: "
)

if __name__ == "__main__":    
    log_msg("print only user log.")
    debug("print and save debug.log file.")
    warning("print only warning message.")