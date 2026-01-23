import sys
import os

def get_python_filename(depth: int = 1):
    try:
        return os.path.basename(sys._getframe(depth).f_code.co_filename)
    except (ValueError, AttributeError):
        return "unknown"

def get_python_codeline(depth: int = 1):
    try:
        return sys._getframe(depth).f_lineno
    except (ValueError, AttributeError):
        return 0