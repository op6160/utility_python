"""
OS & Shell Utility Library

Provides functions to check the operating system (OS) type, detect shell type, and identify shell profile paths.
"""
from .core.os_lib import get_os_type, get_shell_profile, get_shell_type

__all__ = [
    "get_os_type",
    "get_shell_profile",
    "get_shell_type",
]