"""
Browser Automation Library

Provides Selenium-based web browser automation and HTML content retrieval functions.
Uses a driver with bot detection evasion options applied.
"""
from .core.browser_lib.webdriver import get_driver_content
from .core.browser_lib.headers import headers
from .core.browser_lib.connection import connection_test

__all__ = [
    "get_html_content",
    "get_driver_content",
    "headers",
    "connection_test",
]

def get_html_content(url: str, load_time: int = 3) -> str:
    return get_driver_content(url, load_time)