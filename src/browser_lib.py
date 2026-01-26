"""
Browser Automation Library

Provides Selenium-based web browser automation and HTML content retrieval functions.
Uses a driver with bot detection evasion options applied.
"""
from .core.browser_lib.webdriver import get_driver_content, get_driver_mhtml
from .core.browser_lib.headers import headers
from .core.browser_lib.connection import connection_test
from .drive_lib import LocalFileStrategy, save_content as _save_content, load_content as _load_content

__all__ = [
    "get_html_content",
    "save_mhtml",
    "get_driver_content",
    "get_driver_mhtml",
    "headers",
    "connection_test",
    "LocalFileStrategy",
]

def get_html_content(url: str, load_time: int = 3) -> str:
    return get_driver_content(url, load_time)

def save_mhtml(url: str, filename: str, strategy = None, load_time: int = 3) -> None:
    """
    Fetches MHTML content and saves it using the provided strategy.
    Default strategy is LocalFileStrategy.
    """
    content = get_driver_mhtml(url, load_time)
    _save_content(content, filename, strategy)

def load_mhtml(filename: str, strategy = None) -> str:
    """
    Loads MHTML content from a file using the provided strategy.
    Default strategy is LocalFileStrategy.
    """
    return _load_content(filename, strategy)